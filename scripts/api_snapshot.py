"""Consume a reviewed upstream API artifact; never parse or execute Koven code."""
import hashlib
import json
from pathlib import Path
import re
import subprocess

SITE = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True,
                                     separators=(',', ':')).encode()).hexdigest()


def config():
    value = json.loads((SITE / 'api-source.json').read_text())
    if (set(value) != {'repository', 'revision', 'snapshotSha256'}
            or not re.fullmatch(r'[0-9a-f]{40}', value['revision'])
            or not re.fullmatch(r'[0-9a-f]{64}', value['snapshotSha256'])):
        raise ValueError('API source must pin a commit and reviewed snapshot digest')
    # Reuse the existing source identity policy: API and Guide originate in Koven.
    guide = json.loads((SITE / 'content-source.json').read_text())
    if value['repository'].lower() != guide['repository'].lower():
        raise ValueError('API repository does not match reviewed Koven repository')
    return value


def validate(snapshot):
    cfg = config()
    expected = {'repository': 'https://github.com/' + cfg['repository'], 'revision': cfg['revision']}
    if not isinstance(snapshot, dict) or snapshot.get('source') != expected or digest(snapshot) != cfg['snapshotSha256']:
        raise ValueError('API snapshot identity or digest mismatch')
    return snapshot


def build(artifact, root, revision, repository):
    """Bind artifact bytes to actual Git source and derive links, without copying examples."""
    from sync_content import fences, source_repository
    if source_repository(root).lower() != ('https://github.com/' + repository).lower():
        raise ValueError('API checkout repository mismatch')
    def read(path):
        return subprocess.check_output(['git', '-C', str(root), 'show', f'{revision}:{path}']).decode('utf-8')
    if (artifact.get('schema') != 'koven.api-examples' or artifact.get('version') != 1
            or artifact.get('guideVersion') != '0.45'
            or not re.fullmatch(r'[0-9a-f]{64}', artifact.get('compilerSha256', ''))
            or artifact.get('tutorial') != 'docs/tutorials/koven-tour.md'):
        raise ValueError('unsupported API artifact')
    if '<!-- current-guide: v0.45 -->' not in read('docs/guide/README.md'):
        raise ValueError('API Guide does not match artifact')
    text = read(artifact['tutorial'])
    sources = fences(text)
    contracts = {row['id']: row for row in json.loads(read('docs/tutorials/examples.json'))['examples']}
    entries = artifact.get('entries')
    if not isinstance(entries, list) or not entries:
        raise ValueError('API artifact must contain verified entries')
    seen, links = set(), []
    for entry in entries:
        identity = (entry['example'], entry['file'], entry['function'])
        row = contracts.get(entry['example'])
        fence = entry['sourceFence']
        if (identity in seen or row is None or row['status'] != 'executable'
                or row.get('files', {'source.ko': row['id']}).get(entry['file']) != fence):
            raise ValueError('API entry is duplicate or not an executable tutorial binding')
        seen.add(identity)
        source = sources[fence]
        if hashlib.sha256(source.encode()).hexdigest() != entry['sourceSha256']:
            raise ValueError('API source checksum mismatch')
        declaration = entry['declaration']
        location = declaration['location']
        start, end = location['startByte'], location['endByte']
        raw = source.encode()
        if (type(start) is not int or type(end) is not int or not 0 <= start < end <= len(raw)
                or not raw[start:end].decode().startswith(declaration['signature'])
                or declaration['name'] != entry['function']
                or location['line'] != raw[:start].decode().count('\n') + 1):
            raise ValueError('API declaration does not match source range')
        marker = f'```koven {fence}\n'
        if text.count(marker) != 1:
            raise ValueError('API source fence is ambiguous')
        first = text[:text.index(marker)].count('\n') + 2
        line = first + location['line'] - 1
        base = f'https://github.com/{repository}/blob/{revision}/{artifact["tutorial"]}'
        links.append({'source': f'{base}#L{line}', 'example': f'{base}#L{first}'})
    return {'source': {'repository': 'https://github.com/' + repository, 'revision': revision},
            'artifact': artifact, 'links': links}


def load(root=None, artifact_path=None):
    cfg = config()
    if artifact_path is None:
        snapshot = validate(json.loads((SITE / 'src/data/generated.json').read_text())['api'])
        artifact = snapshot['artifact']
    else:
        if root is None:
            raise ValueError('--api-artifact requires --api-source')
        artifact = json.loads(Path(artifact_path).read_text())
        snapshot = None
    if root is not None:
        rebuilt = build(artifact, root, cfg['revision'], cfg['repository'])
        validate(rebuilt)
        if snapshot is not None and rebuilt != snapshot:
            raise ValueError('API snapshot does not match actual source')
        snapshot = rebuilt
    return snapshot
