import unittest
from check_upstream import approved

A, B = 'a' * 40, 'b' * 40
REPO = 'Halckon/koven'


def response(head=A, runs=None):
    if runs is None:
        runs = [dict(head_sha=A, head_branch='main', event='push',
                     status='completed', conclusion='success',
                     path='.github/workflows/ci.yml')]
    def get(path):
        if path.endswith('/git/ref/heads/main'):
            return {'object': {'sha': head}}
        return {'workflow_runs': runs}
    return get


class FreshSource(unittest.TestCase):
    def test_current_success(self):
        self.assertTrue(approved(REPO, A, response()))

    def test_old_success_rerun_and_out_of_order_notification(self):
        self.assertFalse(approved(REPO, A, response(head=B)))

    def test_duplicate_current_notification_is_idempotent(self):
        self.assertTrue(approved(REPO, A, response()))

    def test_build_race_detected_at_deploy(self):
        self.assertTrue(approved(REPO, A, response(head=A)))
        self.assertFalse(approved(REPO, A, response(head=B)))

    def test_missing_or_unverified_ci(self):
        self.assertFalse(approved(REPO, A, response(runs=[])))
        for field, value in [('event', 'pull_request'), ('head_branch', 'feature'),
                             ('head_sha', B), ('conclusion', 'failure'),
                             ('path', 'other.yml'), ('status', 'in_progress')]:
            run = dict(head_sha=A, head_branch='main', event='push',
                       status='completed', conclusion='success',
                       path='.github/workflows/ci.yml')
            run[field] = value
            self.assertFalse(approved(REPO, A, response(runs=[run])), field)

    def test_invalid_sha_fails_closed(self):
        self.assertFalse(approved(REPO, 'main', response()))


if __name__ == '__main__':
    unittest.main()
