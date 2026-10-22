"""Repository identity must follow configuration and the actual checkout."""
import json
import os
import shutil
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

import sync_content as content


class SourceIdentity(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        subprocess.run(['git', 'init', '-q', str(self.root)], check=True)
        (self.root / 'content-source.json').write_text(json.dumps({'repository': 'Example/Source', 'ref': 'main'}))
        self.original_site = content.SITE
        self.site = mock.patch.object(content, 'SITE', self.root)
        self.site.start()
        self.addCleanup(self.site.stop)

    def remote(self, url):
        subprocess.run(['git', '-C', str(self.root), 'config', 'remote.origin.url', url], check=True)

    def test_common_https_and_ssh_forms_keep_configured_identity(self):
        for url in ('https://github.com/example/source', 'https://github.com/example/source.git',
                    'git@github.com:example/source.git', 'ssh://git@github.com/example/source.git'):
            with self.subTest(url=url):
                self.remote(url)
                self.assertEqual(content.source_repository(self.root), 'https://github.com/Example/Source')

    @unittest.skipUnless(os.environ.get('KOVEN_SOURCE'), 'set KOVEN_SOURCE for real repository contract')
    def test_full_generation_keeps_verified_configured_repository(self):
        checkout = self.root / 'source'
        subprocess.run(['git', 'clone', '--quiet', '--shared', '--no-checkout',
                        os.environ['KOVEN_SOURCE'], str(checkout)], check=True)
        subprocess.run(['git', '-C', str(checkout), 'remote', 'set-url', 'origin',
                        'git@github.com:example/source.git'], check=True)
        (self.root / 'scripts').mkdir()
        shutil.copyfile(self.original_site / 'scripts/design-sections.json',
                        self.root / 'scripts/design-sections.json')
        ref = os.environ.get('KOVEN_REF', 'main')
        generated = content.generate(checkout, ref)
        self.assertEqual(generated['source']['repository'], 'https://github.com/Example/Source')
        self.assertEqual(generated['source']['revision'], subprocess.check_output(
            ['git', '-C', str(checkout), 'rev-parse', ref + '^{commit}'], text=True).strip())
        content.validate_snapshot(generated)

    def test_other_repository_or_host_and_credentials_are_rejected(self):
        for url in ('https://github.com/elsewhere/source.git', 'https://example.com/example/source.git',
                    'https://token@github.com/example/source.git', '/tmp/local-clone'):
            with self.subTest(url=url):
                self.remote(url)
                with self.assertRaises(ValueError) as failure:
                    content.source_repository(self.root)
                self.assertNotIn(url, str(failure.exception))

    def test_missing_origin_is_rejected(self):
        with self.assertRaises(ValueError):
            content.source_repository(self.root)

    def test_invalid_config_is_rejected(self):
        (self.root / 'content-source.json').write_text(json.dumps({'repository': 'bad\nsource', 'ref': 'main'}))
        self.remote('https://github.com/example/source.git')
        with self.assertRaises(ValueError):
            content.source_repository(self.root)


class SnapshotIdentity(unittest.TestCase):
    def test_offline_snapshot_cannot_claim_another_repository(self):
        data = json.loads((content.SITE / 'src/data/generated.json').read_text())
        data['source']['repository'] = 'https://github.com/elsewhere/source'
        with self.assertRaisesRegex(ValueError, 'repository'):
            content.validate_snapshot(data)


if __name__ == '__main__':
    unittest.main()
