"""Resolve a reviewed source configuration without accepting arbitrary dispatch refs."""
import json
import os
from pathlib import Path
import re


def resolve(config, event_name, event):
    repository, ref = config['repository'], config['ref']
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise ValueError('invalid configured repository')
    if not re.fullmatch(r'[A-Za-z0-9_./-]+', ref) or ref.startswith('-'):
        raise ValueError('invalid configured ref')
    nightly = ref == 'main'
    if nightly and event_name == 'repository_dispatch':
        payload = event.get('client_payload', {})
        sha = payload.get('sha', '')
        if (payload.get('repository', '').casefold() != repository.casefold()
                or not re.fullmatch(r'[0-9a-f]{40}', sha)):
            raise ValueError('nightly notification must identify the configured repository and commit')
        ref = sha
    return {'repository': repository, 'ref': ref, 'nightly': str(nightly).lower()}


if __name__ == '__main__':
    config = json.loads(Path('content-source.json').read_text())
    event = json.loads(Path(os.environ['GITHUB_EVENT_PATH']).read_text())
    result = resolve(config, os.environ['GITHUB_EVENT_NAME'], event)
    for key, value in result.items():
        print(f'{key}={value}')
