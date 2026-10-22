#!/usr/bin/env python3
"""Build website data from one immutable Koven Git revision; never execute source code."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import shlex
import subprocess

SITE = Path(__file__).resolve().parents[1]
REPO = 'https://github.com/Halckon/koven'


def fences(text):
    blocks = re.findall(r'^```koven ([a-z0-9-]+)\n(.*?)^```$', text, re.M | re.S)
    if len(dict(blocks)) != len(blocks):
        raise ValueError('duplicate tutorial source fence')
    return dict(blocks)


def section(markdown, title):
    """Require a real Markdown heading before publishing a dependent lesson."""
    lines = markdown.splitlines()
    start = next((i for i, line in enumerate(lines)
                  if re.fullmatch(r'#{2,6} ' + re.escape(title), line)), None)
    if start is None:
        raise ValueError(f'Guide section not found: {title}')
    depth = len(lines[start]) - len(lines[start].lstrip('#'))
    end = next((i for i in range(start + 1, len(lines))
                if re.match(r'#{1,' + str(depth) + r'} ', lines[i])), len(lines))
    return '\n'.join(lines[start + 1:end]).strip()


def design_lessons(pages, version):
    selections = json.loads((SITE / 'scripts/design-sections.json').read_text())
    result = []
    for lesson_id, title, file, heading in selections:
        page = next((page for page in pages if page['file'] == file), None)
        if page is None:
            raise ValueError(f'Guide page not found: {file}')
        result.append({'id': lesson_id, 'title': title.format(version=version), 'path': page['path'],
                       'markdown': section(page['markdown'], heading.format(version=version))})
    return result


def validate_snapshot(data):
    if design_lessons(data['specPages'], data['source']['version']) != data['designLessons']:
        raise ValueError('design curriculum changed; regenerate content before building')
    for page in data['specPages']:
        if hashlib.sha256(page['markdown'].encode()).hexdigest() != data['source']['hashes'][page['path']]:
            raise ValueError('Guide snapshot checksum mismatch')


def examples(rows, sources):
    output, references = [], []
    for row in rows:
        status = row['status']
        if status not in ('executable', 'diagnostic', 'planned'):
            raise ValueError('unknown example status')
        files = row.get('files', {'source.ko': row['id']})
        if not files or row['id'] not in files.values():
            raise ValueError('example must reference its own source')
        for path, source in files.items():
            parsed = PurePosixPath(path)
            if parsed.is_absolute() or '..' in parsed.parts or parsed.suffix != '.ko' or source not in sources:
                raise ValueError('invalid tutorial source path or missing fence')
            references.append(source)
        commands, cases, diagnostics = [], [], []
        manifest = ''
        if status != 'planned':
            if 'files' in row:
                entry = row.get('entry')
                if not entry:
                    raise ValueError('project entry missing')
                inputs = ['--project', 'project.toml', '--entry', entry]
                manifest = 'schema = "koven.project"\nversion = 1\n\n[project]\nname = "tutorial"\nsource-roots = ["src"]\n'
            else:
                inputs = ['source.ko']
            commands.append(shlex.join(['kovenc', *(['--message-format=json'] if status == 'diagnostic' else []), 'build', *inputs, '-o', 'program']))
            if status == 'diagnostic':
                diagnostics = [json.loads(line) for line in row['build']['stderr'].splitlines()]
                if row['build']['exit'] == 0 or not diagnostics:
                    raise ValueError('diagnostic contract must fail with structured diagnostics')
            else:
                for case in row.get('cases', [row]):
                    cases.append({'args': case['args'], 'stdout': case['run']['stdout'],
                                  'stderr': case['run']['stderr'], 'exit': case['run']['exit'],
                                  'command': shlex.join(['kovenc', 'run', *inputs, '--', *case['args']])})
        output.append({'id': row['id'], 'status': status, 'reason': row.get('reason', ''),
                       'files': [{'path': path, 'code': sources[source]} for path, source in files.items()],
                       'manifest': manifest, 'commands': commands, 'cases': cases, 'diagnostics': diagnostics})
    if len({x['id'] for x in rows}) != len(rows) or len(set(references)) != len(references) or set(references) != set(sources):
        raise ValueError('tutorial source/contract identity mismatch')
    return output


def generate(root, ref):
    def git(*args):
        return subprocess.check_output(['git', '-C', str(root), *args]).decode('utf-8')
    revision = git('rev-parse', '--verify', ref + '^{commit}').strip()
    hashes = {}
    def read(path):
        content = git('show', f'{revision}:{path}')
        hashes[path] = hashlib.sha256(content.encode()).hexdigest()
        return content
    tutorial_path = 'docs/tutorials/koven-tour.md'
    tutorial = read(tutorial_path)
    inventory = json.loads(read('docs/tutorials/examples.json'))
    if inventory['version'] != 1:
        raise ValueError('unsupported tutorial contract version')
    guide = read('docs/guide/README.md')
    version_match = re.search(r'<!-- current-guide: (v[0-9.]+) -->', guide)
    if not version_match:
        raise ValueError('current Guide version marker missing')
    pages = re.findall(r'^\| (.+?) \| \[(.+?)\]\((\d\d-[^)]+\.md)\) \|$', guide, re.M)
    if len(pages) != 15:
        raise ValueError('Guide index changed; review importer before publishing')
    spec_pages = []
    for description, title, file in pages:
        path = 'docs/guide/' + file
        spec_pages.append({'file': file, 'title': title, 'description': description,
                           'markdown': read(path), 'path': path})
    chapters = []
    for match in re.finditer(r'^## ([a-z0-9-]+)\n(.*?)(?=^## |\Z)', tutorial, re.M | re.S):
        chapter_id, body = match.groups()
        # Executable code comes exclusively from the contract files shown by the viewer.
        prose = re.sub(r'^```koven [a-z0-9-]+\n.*?^```\n?', '', body, flags=re.M | re.S).strip()
        chapters.append({'id': chapter_id, 'markdown': prose, 'path': tutorial_path})
    roadmap = json.loads(read('docs/roadmap/v1.json'))
    return {'source': {'repository': REPO, 'ref': ref, 'revision': revision,
                       'version': version_match[1], 'hashes': hashes},
            'chapters': chapters, 'examples': examples(inventory['examples'], fences(tutorial)),
            'specPages': spec_pages, 'designLessons': design_lessons(spec_pages, version_match[1]),
            'roadmap': roadmap}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--source', type=Path)
    parser.add_argument('--ref', help='main for nightly, a tag for stable, or an explicitly selected design revision')
    parser.add_argument('--check', action='store_true')
    parser.add_argument('--validate-snapshot', action='store_true')
    args = parser.parse_args()
    destination = SITE / 'src/data/generated.json'
    if args.validate_snapshot:
        validate_snapshot(json.loads(destination.read_text()))
        print('snapshot and design sections verified')
        raise SystemExit(0)
    if not args.source or not args.ref:
        parser.error('--source and --ref are required for synchronization')
    content = json.dumps(generate(args.source, args.ref), ensure_ascii=False, indent=2) + '\n'
    if args.check:
        if not destination.exists() or destination.read_text() != content:
            raise SystemExit('generated content is stale; run sync-content')
    else:
        destination.write_text(content)
    print('content verified' if args.check else 'content synchronized')
