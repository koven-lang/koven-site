"""Independent contract mutations catch false completion and broken traceability."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from check_docs import check

ROOT = Path(__file__).resolve().parents[1]
PREFIX = '<!-- metadata: '
SPEC_SECTIONS = ('目标', '范围', '非目标', '行为合同', '接口变化', '失败场景', '依赖', '测试与验收', '完成条件', '验收证据')
MILESTONE_SECTIONS = ('目标', '范围', '非目标', '基线', '依赖', '联合验收', '完成条件', '验收证据')


class GovernanceContracts(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.inventory = {
            'SITE-V1-M0': 'docs/milestones/active/SITE-V1-M0.md',
            'SPEC-0001': 'docs/specs/active/0001.md',
            'SPEC-0002': 'docs/specs/drafts/0002.md',
        }
        self.write('SITE-V1-M0', {
            'kind': 'milestone', 'status': 'in-progress', 'specs': ['SPEC-0001', 'SPEC-0002'],
            'depends_on': [], 'blockers': [], 'evidence': [],
        })
        self.write('SPEC-0001', {
            'kind': 'spec', 'status': 'in-progress', 'milestone': 'SITE-V1-M0',
            'depends_on': [], 'blockers': [], 'evidence': [],
        })
        self.write('SPEC-0002', {
            'kind': 'spec', 'status': 'draft', 'milestone': 'SITE-V1-M0',
            'depends_on': ['SPEC-0001'], 'blockers': [], 'evidence': [],
        })
        (self.root / 'docs/evidence.md').write_text('# 可追溯结果\n\nfixture evidence\n')
        self.save_inventory()

    def save_inventory(self):
        (self.root / 'docs/inventory.json').write_text(json.dumps(self.inventory))

    def path(self, identity):
        return self.root / self.inventory[identity]

    def write(self, identity, meta):
        path = self.path(identity)
        path.parent.mkdir(parents=True, exist_ok=True)
        meta = dict(id=identity, **meta)
        sections = SPEC_SECTIONS if meta['kind'] == 'spec' else MILESTONE_SECTIONS
        path.write_text(PREFIX + json.dumps(meta) + ' -->\n# 合同\n\n'
                        + ''.join(f'## {name}\n\n具体验收合同。\n\n' for name in sections))

    def change(self, identity, **changes):
        path = self.path(identity)
        lines = path.read_text().splitlines()
        meta = json.loads(lines[0][len(PREFIX):-len(' -->')])
        meta.update(changes)
        lines[0] = PREFIX + json.dumps(meta) + ' -->'
        path.write_text('\n'.join(lines) + '\n')

    def move(self, identity, relative):
        old = self.path(identity)
        new = self.root / relative
        new.parent.mkdir(parents=True, exist_ok=True)
        old.rename(new)
        self.inventory[identity] = relative
        self.save_inventory()

    def rejects(self, phrase):
        errors = check(self.root)
        self.assertTrue(any(phrase in error for error in errors), errors)

    def test_valid_site_contract_tree(self):
        self.assertEqual([], check(self.root))

    def test_cannot_activate_spec_until_local_dependency_done(self):
        self.change('SPEC-0002', status='approved')
        self.move('SPEC-0002', 'docs/specs/active/0002.md')
        self.rejects('unfinished dependency')

    def test_active_spec_cannot_have_blockers(self):
        self.change('SPEC-0001', blockers=['missing reviewed producer contract'])
        self.rejects('blockers')

    def test_progressive_planning_does_not_require_placeholder_specs(self):
        self.path('SPEC-0002').unlink()
        del self.inventory['SPEC-0002']
        self.save_inventory()
        self.change('SITE-V1-M0', specs=['SPEC-0001'])
        self.assertEqual([], check(self.root))

    def test_duplicate_inventory_id(self):
        p = self.root / 'docs/inventory.json'
        p.write_text(p.read_text().replace('{', '{"SPEC-0001":"docs/specs/active/0001.md",', 1))
        self.rejects('duplicate JSON key')

    def test_empty_inventory_is_not_a_success(self):
        (self.root / 'docs/inventory.json').write_text('{}')
        self.rejects('non-empty object')

    def test_unregistered_contract(self):
        p = self.root / 'docs/specs/drafts/0999.md'
        p.write_text('# 不能绕过库存\n')
        self.rejects('unregistered document')

    def test_duplicated_or_misplaced_metadata(self):
        (self.root / 'docs/duplicate.md').write_text(self.path('SPEC-0001').read_text())
        self.rejects('unregistered metadata')
        self.rejects('duplicate document ID')

    def test_membership_is_bidirectional(self):
        self.change('SITE-V1-M0', specs=['SPEC-0001'])
        self.rejects('membership mismatch')

    def test_unknown_dependency(self):
        self.change('SPEC-0002', depends_on=['SPEC-9999'])
        self.rejects('unknown dependency')

    def test_dependency_kind_cannot_mix_spec_and_milestone(self):
        self.change('SPEC-0002', depends_on=['SITE-V1-M0'])
        self.rejects('dependency kind mismatch')

    def test_dependency_cycle(self):
        self.change('SPEC-0001', depends_on=['SPEC-0002'])
        self.rejects('dependency cycle')

    def test_status_must_match_location(self):
        self.change('SPEC-0001', status='done', evidence=['docs/evidence.md'])
        self.rejects('status/location mismatch')

    def test_completion_requires_evidence(self):
        self.change('SPEC-0001', status='done')
        self.move('SPEC-0001', 'docs/archive/specs/0001.md')
        self.rejects('completion evidence required')

    def test_missing_evidence_file(self):
        self.change('SPEC-0001', evidence=['missing.md'])
        self.rejects('missing evidence')

    def test_milestone_cannot_close_with_open_specs(self):
        self.change('SITE-V1-M0', status='completed', evidence=['docs/evidence.md'])
        self.move('SITE-V1-M0', 'docs/archive/milestones/SITE-V1-M0.md')
        self.rejects('unfinished child')

    def test_milestone_requires_multiple_completed_specs(self):
        self.path('SPEC-0002').unlink()
        del self.inventory['SPEC-0002']
        self.change('SPEC-0001', status='done', evidence=['docs/evidence.md'])
        self.move('SPEC-0001', 'docs/archive/specs/0001.md')
        self.change('SITE-V1-M0', status='completed', specs=['SPEC-0001'], evidence=['docs/evidence.md'])
        self.move('SITE-V1-M0', 'docs/archive/milestones/SITE-V1-M0.md')
        self.rejects('multiple specs')

    def test_complete_archive_transition(self):
        for identity, number in [('SPEC-0001', '0001'), ('SPEC-0002', '0002')]:
            self.change(identity, status='done', evidence=['docs/evidence.md'])
            self.move(identity, f'docs/archive/specs/{number}.md')
        self.change('SITE-V1-M0', status='completed', evidence=['docs/evidence.md'])
        self.move('SITE-V1-M0', 'docs/archive/milestones/SITE-V1-M0.md')
        self.assertEqual([], check(self.root))

    def test_metadata_field_types(self):
        self.change('SPEC-0001', depends_on='SPEC-0002')
        self.rejects('list of strings')

    def test_path_cannot_escape_repository(self):
        self.inventory['SPEC-0001'] = '../outside.md'
        self.save_inventory()
        self.rejects('unsafe path')

    def test_duplicate_inventory_path(self):
        self.inventory['SPEC-0002'] = self.inventory['SPEC-0001']
        self.save_inventory()
        self.rejects('duplicate inventory path')

    def test_required_section(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text().replace('## 失败场景', '## 缺少失败场景'))
        self.rejects('missing section')

    def test_invalid_utf8_is_a_check_failure(self):
        self.path('SPEC-0001').write_bytes(b'\xff')
        self.rejects('UTF-8')

    def test_broken_link(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[missing](missing.md)\n')
        self.rejects('broken link')

    def test_broken_reference_link(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[missing][nope]\n\n[nope]: missing.md\n')
        self.rejects('broken link')

    def test_archive_cannot_leave_broken_root_entrypoint(self):
        (self.root / 'README.md').write_text('[SPEC](docs/specs/active/0001.md)\n')
        self.change('SPEC-0001', status='done', evidence=['docs/evidence.md'])
        self.move('SPEC-0001', 'docs/archive/specs/0001.md')
        self.rejects('broken link')

    def test_titled_inline_target_is_checked(self):
        (self.root / 'README.md').write_text('[合同](missing.md "合同标题")\n')
        self.rejects('broken link')

    def test_titled_inline_anchor_is_checked(self):
        (self.root / 'README.md').write_text('[合同](docs/evidence.md#missing "合同标题")\n')
        self.rejects('broken anchor')

    def test_titled_and_angle_inline_links_are_valid(self):
        (self.root / 'README.md').write_text('[合同](docs/evidence.md "标题")\n[证据](<docs/evidence.md#可追溯结果> "标题")\n')
        self.assertEqual(check(self.root), [])

    def test_shortcut_reference_target_is_checked(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[合同]\n\n[合同]: missing-contract.md\n')
        self.rejects('broken link')

    def test_shortcut_reference_anchor_is_checked(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[合同]\n\n[合同]: #missing-section\n')
        self.rejects('broken anchor')

    def test_undefined_reference_link(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[missing][nope]\n')
        self.rejects('missing link reference')

    def test_broken_anchor(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[missing](#missing)\n')
        self.rejects('broken anchor')

    def test_chinese_anchor_and_fenced_example(self):
        p = self.path('SPEC-0001')
        p.write_text(p.read_text() + '\n[行为](#行为合同)\n\n```md\n[example](missing.md)\n```\n')
        self.assertEqual([], check(self.root))

    def test_cli_exit_status(self):
        command = [sys.executable, str(ROOT / 'scripts/check_docs.py'), '--root', str(self.root)]
        success = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(success.returncode, 0, success.stderr)
        self.change('SPEC-0001', blockers=['contract missing'])
        failed = subprocess.run(command, capture_output=True, text=True)
        self.assertEqual(failed.returncode, 1, failed.stderr)
        self.assertIn('blockers', failed.stderr)


if __name__ == '__main__':
    unittest.main()
