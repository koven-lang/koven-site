import copy
import json
import os
from pathlib import Path
import unittest
import api_snapshot as api

class ApiSnapshotTests(unittest.TestCase):
    def test_real_snapshot_and_tampering(self):
        data = json.loads((Path(__file__).parents[1] / 'src/data/generated.json').read_text())['api']
        api.validate(data)
        for mutate in (lambda d: d['artifact'].update(version=9),
                       lambda d: d['artifact']['entries'][0]['declaration'].update(signature='forged'),
                       lambda d: d['source'].update(revision='main'),
                       lambda d: d['links'][0].update(source='javascript:alert(1)')):
            bad = copy.deepcopy(data)
            mutate(bad)
            with self.assertRaises(ValueError):
                api.validate(bad)

    @unittest.skipUnless(os.environ.get('KOVEN_API_SOURCE'), 'requires real API source checkout')
    def test_real_source_rebuild_and_rejected_bindings(self):
        data = api.load(Path(os.environ['KOVEN_API_SOURCE']))
        cfg = api.config()
        for mutate in (lambda a: a.update(entries=[]),
                       lambda a: a['entries'].append(copy.deepcopy(a['entries'][0])),
                       lambda a: a['entries'][0].update(sourceSha256='0' * 64),
                       lambda a: a['entries'][0]['declaration'].update(signature='forged'),
                       lambda a: a['entries'][0].update(example='planned-thread')):
            bad = copy.deepcopy(data['artifact'])
            mutate(bad)
            with self.assertRaises(ValueError):
                api.build(bad, Path(os.environ['KOVEN_API_SOURCE']), cfg['revision'], cfg['repository'])

if __name__ == '__main__':
    unittest.main()
