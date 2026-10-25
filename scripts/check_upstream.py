"""Fail closed if a dynamic Guide source is not the current CI-approved main."""
import json
import re
import subprocess
import sys


def api(path):
    out = subprocess.check_output(['gh', 'api', path], text=True)
    return json.loads(out)


def approved(repository, sha, get=api):
    if not re.fullmatch(r'[0-9a-f]{40}', sha):
        return False
    # Strict freshness: old CI reruns / out-of-order dispatches never select old main.
    head = get(f'repos/{repository}/git/ref/heads/main')['object']['sha']
    if head != sha:
        return False
    # Do not trust client_payload's conclusion, run ID, or its asserted SHA.
    runs = get(f'repos/{repository}/actions/workflows/ci.yml/runs?head_sha={sha}&event=push&status=success&per_page=100')
    return any(run.get('head_sha') == sha
               and run.get('head_branch') == 'main'
               and run.get('event') == 'push'
               and run.get('status') == 'completed'
               and run.get('conclusion') == 'success'
               and run.get('path') == '.github/workflows/ci.yml'
               for run in runs.get('workflow_runs', []))


def main():
    repository, sha = sys.argv[1:3]
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+', repository):
        raise SystemExit('invalid repository')
    if not approved(repository, sha):
        raise SystemExit(f'reject stale or unverified Guide source {repository}@{sha}')
    print(f'approved Guide source {repository}@{sha}')


if __name__ == '__main__':
    main()
