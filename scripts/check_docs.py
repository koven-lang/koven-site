#!/usr/bin/env python3
"""Validate inventory, lifecycle and traceability; evidence truth needs review."""
import argparse
import json
from pathlib import Path
import re
import sys
from urllib.parse import unquote
import unicodedata

SECTIONS = {
    'spec': ('目标', '范围', '非目标', '行为合同', '接口变化', '失败场景', '依赖', '测试与验收', '完成条件', '验收证据'),
    'milestone': ('目标', '范围', '非目标', '基线', '依赖', '联合验收', '完成条件', '验收证据'),
}
STATES = {
    'spec': {'draft': 'docs/specs/drafts', 'approved': 'docs/specs/active', 'in-progress': 'docs/specs/active', 'done': 'docs/archive/specs', 'superseded': 'docs/archive/specs'},
    'milestone': {'draft': 'docs/milestones/drafts', 'approved': 'docs/milestones/active', 'in-progress': 'docs/milestones/active', 'completed': 'docs/archive/milestones', 'cancelled': 'docs/archive/milestones'},
}
PREFIX = '<!-- metadata: '


def unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f'duplicate JSON key: {key}')
        result[key] = value
    return result


def read_json(text):
    return json.loads(text, object_pairs_hook=unique_object)


def safe_file(root, value):
    if not isinstance(value, str) or not value or Path(value).is_absolute():
        raise ValueError(f'unsafe path: {value!r}')
    path = root / value
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'unsafe path: {value!r}')
    return path


def check(root):
    root = Path(root).resolve()
    errors = []
    try:
        inventory = read_json((root / 'docs/inventory.json').read_text(encoding='utf-8'))
        if not isinstance(inventory, dict) or not inventory:
            raise ValueError('inventory must be a non-empty object')
    except (OSError, ValueError) as error:
        return [f'docs/inventory.json: {error}']
    records = {}
    paths = set()

    def read_document(path):
        """Report malformed input without aborting the rest of the inventory audit."""
        try:
            if not path.resolve().is_relative_to(root):
                raise ValueError('unsafe document path')
            return path.read_text(encoding='utf-8')
        except (OSError, ValueError) as error:
            errors.append(f'{path.relative_to(root)}: cannot read UTF-8 document: {error}')
            return None

    for identity, relative in inventory.items():
        try:
            path = safe_file(root, relative)
            if path.resolve() in paths:
                raise ValueError('duplicate inventory path')
            paths.add(path.resolve())
            text = read_document(path)
            if text is None:
                continue
            first = text.splitlines()[0] if text else ''
            if not first.startswith(PREFIX) or not first.endswith(' -->'):
                raise ValueError('missing metadata header')
            meta = read_json(first[len(PREFIX):-len(' -->')])
            if not isinstance(meta, dict):
                raise ValueError('metadata must be object')
            kind = meta.get('kind')
            if kind not in SECTIONS:
                raise ValueError('invalid kind')
            pattern = r'SPEC-\d{4}' if kind == 'spec' else r'SITE-V1-M\d+'
            if not re.fullmatch(pattern, identity) or meta.get('id') != identity:
                raise ValueError('invalid or mismatched ID')
            for field in ('depends_on', 'blockers', 'evidence') + (('specs',) if kind == 'milestone' else ()):
                value = meta.get(field)
                if not isinstance(value, list) or any(not isinstance(v, str) or not v.strip() for v in value):
                    raise ValueError(f'{field} must be list of strings')
                if len(value) != len(set(value)):
                    raise ValueError(f'duplicate {field}')
            if kind == 'spec' and not isinstance(meta.get('milestone'), str):
                raise ValueError('milestone must be string')
            if not isinstance(meta.get('status'), str):
                raise ValueError('status must be string')
            expected = STATES[kind].get(meta['status'])
            if expected is None or path.parent != root / expected:
                errors.append(f'{relative}: status/location mismatch')
            for section in SECTIONS[kind]:
                match = re.search(r'^## ' + re.escape(section) + r'\n(.*?)(?=^## |\Z)', text, re.M | re.S)
                if not match or not match[1].strip():
                    errors.append(f'{relative}: missing section {section}')
            for evidence in meta['evidence']:
                if not safe_file(root, evidence).is_file():
                    errors.append(f'{relative}: missing evidence {evidence}')
            records[identity] = meta
        except (OSError, ValueError, TypeError) as error:
            errors.append(f'{identity}: {error}')

    markdown_files = sorted([*(root / 'docs').rglob('*.md'), *root.glob('*.md')])
    # Include root entrypoints so archiving cannot silently break their links.
    seen_ids = {}
    for path in markdown_files:
        text = read_document(path)
        if text is None:
            continue
        if text.startswith(PREFIX):
            if path.resolve() not in paths:
                errors.append(f'{path.relative_to(root)}: unregistered metadata document')
            try:
                identity = read_json(text.splitlines()[0][len(PREFIX):-len(' -->')]).get('id')
                if identity in seen_ids:
                    errors.append(f'{path.relative_to(root)}: duplicate document ID {identity}')
                seen_ids[identity] = path
            except (ValueError, TypeError, AttributeError):
                errors.append(f'{path.relative_to(root)}: invalid metadata')
    # Also reject metadata-less files placed among lifecycle contracts.
    for folder in ('docs/specs/drafts', 'docs/specs/active', 'docs/archive/specs', 'docs/milestones/drafts', 'docs/milestones/active', 'docs/archive/milestones'):
        for path in sorted((root / folder).rglob('*.md')):
            if path.resolve() not in paths:
                errors.append(f'{path.relative_to(root)}: unregistered document')
    for identity, meta in records.items():
        kind = meta['kind']
        if kind == 'spec':
            parent = records.get(meta['milestone'], {})
            if parent.get('kind') != 'milestone' or identity not in parent.get('specs', []):
                errors.append(f'{identity}: membership mismatch')
        else:
            if meta['status'] == 'completed' and len(meta['specs']) < 2:
                errors.append(f'{identity}: milestone requires multiple specs')
            for child in meta['specs']:
                target = records.get(child, {})
                if target.get('kind') != 'spec' or target.get('milestone') != identity:
                    errors.append(f'{identity}: membership mismatch {child}')
        for dependency in meta['depends_on']:
            if dependency not in records:
                errors.append(f'{identity}: unknown dependency {dependency}')
            elif records[dependency]['kind'] != kind:
                errors.append(f'{identity}: dependency kind mismatch {dependency}')
        complete = meta['status'] in ('done', 'completed')
        activated = kind == 'spec' and meta['status'] in ('approved', 'in-progress')
        if complete or activated:
            if meta['blockers']:
                errors.append(f'{identity}: cannot proceed with blockers')
            for dependency in meta['depends_on']:
                if records.get(dependency, {}).get('status') not in ('done', 'completed'):
                    errors.append(f'{identity}: unfinished dependency {dependency}')
        if complete:
            if not meta['evidence']:
                errors.append(f'{identity}: completion evidence required')
            for child in meta.get('specs', []):
                if records.get(child, {}).get('status') != 'done':
                    errors.append(f'{identity}: unfinished child {child}')

    visited, active = set(), set()
    def visit(identity):
        if identity in active:
            errors.append(f'{identity}: dependency cycle')
            return
        if identity in visited or identity not in records:
            return
        active.add(identity)
        for dependency in records[identity]['depends_on']:
            visit(dependency)
        active.remove(identity)
        visited.add(identity)
    for identity in records:
        visit(identity)

    # Check inline links and all reference definitions, including shortcut references.
    def prose(text):
        return re.sub(r'^```[^\n]*\n.*?^```[^\n]*$', '', text, flags=re.M | re.S)

    def anchors(text):
        counts, result = {}, set()
        for heading in re.findall(r'^#{1,6} +(.+)$', prose(text), re.M):
            slug = ''.join(c for c in heading.lower().strip() if c in '-_ ' or unicodedata.category(c)[0] in 'LN').replace(' ', '-')
            count = counts.get(slug, 0)
            counts[slug] = count + 1
            result.add(slug if not count else f'{slug}-{count}')
        return result

    for path in markdown_files:
        document = read_document(path)
        if document is None:
            continue
        text = prose(document)
        hrefs = re.findall(r'\]\(\s*(<[^>\n]+>|[^\s)]+)', text)
        definitions = re.findall(r'^\[([^]]+)\]:\s*(<[^>\n]+>|\S+)', text, re.M)
        references = {key.casefold(): value for key, value in definitions}
        hrefs.extend(value for _, value in definitions)
        for label, key in re.findall(r'\[([^]\n]+)\]\[([^]\n]*)\]', text):
            key = (key or label).casefold()
            if key not in references:
                errors.append(f'{path.relative_to(root)}: missing link reference {key}')
        for href in hrefs:
            if href.startswith('<') and href.endswith('>'):
                href = href[1:-1]
            if href.startswith(('https://', 'http://', 'mailto:')):
                continue
            target, _, fragment = href.partition('#')
            resolved = path.parent / unquote(target) if target else path
            if not resolved.resolve().is_relative_to(root) or not resolved.is_file():
                errors.append(f'{path.relative_to(root)}: broken link {href}')
            elif fragment and resolved.suffix == '.md':
                target_text = read_document(resolved)
                if target_text is not None and unquote(fragment) not in anchors(target_text):
                    errors.append(f'{path.relative_to(root)}: broken anchor {href}')
    return errors


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    errors = check(args.root)
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        return 1
    print('Documentation contracts passed.')
    return 0


if __name__ == '__main__':
    sys.exit(main())
