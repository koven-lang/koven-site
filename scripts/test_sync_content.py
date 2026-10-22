import importlib.util
import os
import json
import subprocess
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sync_content', Path(__file__).with_name('sync_content.py'))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ContentContracts(unittest.TestCase):
    def test_renamed_guide_section_fails_before_build(self):
        with self.assertRaisesRegex(ValueError, 'Guide section not found'):
            module.section('## v0.46 启用范围\nbody\n', 'v0.46 启用边界')

    def test_section_stops_at_same_depth_heading(self):
        self.assertEqual(module.section('## a\nbody\n### child\ntext\n## b\nnext', 'a'),
                         'body\n### child\ntext')

    def test_duplicate_fence_fails(self):
        with self.assertRaises(ValueError):
            module.fences('```koven hello\nx\n```\n```koven hello\ny\n```\n')

    def test_unknown_source_fails(self):
        with self.assertRaises(ValueError):
            module.examples([{'id': 'missing', 'status': 'executable'}], {})

    def test_planned_never_gets_run_commands(self):
        result = module.examples([{'id': 'later', 'status': 'planned', 'reason': 'not delivered'}], {'later': 'fun main() {}'})
        self.assertEqual(result[0]['commands'], [])
        self.assertEqual(result[0]['cases'], [])

    def test_project_paths_cannot_escape(self):
        with self.assertRaises(ValueError):
            module.examples([{'id': 'x', 'status': 'executable', 'entry': 'app.main',
                              'files': {'../x.ko': 'x'}}], {'x': 'x'})

    @unittest.skipUnless(os.environ.get('KOVEN_SOURCE'), 'set KOVEN_SOURCE for real repository contract')
    def test_real_inventory_and_source_identity(self):
        root = Path(os.environ['KOVEN_SOURCE'])
        result = module.generate(root, os.environ.get('KOVEN_REF', 'main'))
        ref = os.environ.get('KOVEN_REF', 'main')
        inventory = json.loads(subprocess.check_output(['git', '-C', str(root), 'show', ref + ':docs/tutorials/examples.json'], text=True))['examples']
        self.assertEqual([x['id'] for x in result['examples']], [x['id'] for x in inventory])
        self.assertEqual(len(result['specPages']), 15)
        self.assertEqual([x['status'] for x in result['examples']], [x['status'] for x in inventory])
        self.assertTrue(any(x['id'] == 'collections-and-borrow-results' for x in result['chapters']))
        for row in result['examples']:
            if row['status'] == 'planned':
                self.assertFalse(row['commands'])
        self.assertEqual(result, module.generate(root, os.environ.get('KOVEN_REF', 'main')))
        module.validate_snapshot(result)


if __name__ == '__main__':
    unittest.main()
