import unittest
from resolve_source import resolve


class SourceResolution(unittest.TestCase):
    def test_nightly_pins_the_notified_commit(self):
        result = resolve({'repository': 'Halckon/koven', 'ref': 'main'}, 'repository_dispatch',
                         {'client_payload': {'repository': 'Halckon/Koven', 'sha': 'a' * 40, 'ref': 'evil'}})
        self.assertEqual(result['ref'], 'a' * 40)
        self.assertEqual(result['nightly'], 'true')

    def test_dispatch_cannot_change_configured_repository(self):
        with self.assertRaises(ValueError):
            resolve({'repository': 'Halckon/koven', 'ref': 'main'}, 'repository_dispatch',
                    {'client_payload': {'repository': 'other/repo', 'sha': 'a' * 40}})

    def test_tag_and_design_pin_ignore_dispatch_ref(self):
        for ref in ['v1.0.0', 'b' * 40]:
            self.assertEqual(resolve({'repository': 'Halckon/koven', 'ref': ref}, 'repository_dispatch',
                                     {'client_payload': {'ref': 'evil'}})['ref'], ref)

    def test_malformed_commit_is_rejected(self):
        with self.assertRaises(ValueError):
            resolve({'repository': 'Halckon/koven', 'ref': 'main'}, 'repository_dispatch',
                    {'client_payload': {'repository': 'Halckon/koven', 'sha': 'main'}})


if __name__ == '__main__':
    unittest.main()
