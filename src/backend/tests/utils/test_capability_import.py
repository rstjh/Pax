from unittest import TestCase

from utils.CapabilityImport import parse_capability_document


class TestParseCapabilityDocument(TestCase):
    """
    Parses tests/data/sample_capability.docx, a synthetic fixture with the
    same Heading-style + literal-numbering convention as the real capability
    Word document described in the requirements (not available in this
    repo — validate against the team's actual document once it's provided).
    """

    def setUp(self):
        with open('./tests/data/sample_capability.docx', 'rb') as sample_file:
            self.capabilities = parse_capability_document(sample_file)

    def test_imports_every_heading(self):
        self.assertEqual(len(self.capabilities), 7)

    def test_ref_codes_and_levels(self):
        by_ref_code = {c['refCode']: c for c in self.capabilities}
        self.assertEqual(by_ref_code['1']['level'], 1)
        self.assertEqual(by_ref_code['1']['name'], 'Finance')
        self.assertEqual(by_ref_code['1.1']['level'], 2)
        self.assertEqual(by_ref_code['1.1']['name'], 'Payroll Management')
        self.assertEqual(by_ref_code['1.1.1']['level'], 3)
        self.assertEqual(by_ref_code['1.1.1']['name'], 'Payroll Processing')

    def test_parent_linkage(self):
        by_ref_code = {c['refCode']: c for c in self.capabilities}
        self.assertIsNone(by_ref_code['1']['parentRefCode'])
        self.assertEqual(by_ref_code['1.1']['parentRefCode'], '1')
        self.assertEqual(by_ref_code['1.1.1']['parentRefCode'], '1.1')
        self.assertEqual(by_ref_code['1.1.2']['parentRefCode'], '1.1')
        self.assertEqual(by_ref_code['1.2']['parentRefCode'], '1')
        self.assertEqual(by_ref_code['2']['parentRefCode'], None)
        self.assertEqual(by_ref_code['2.1']['parentRefCode'], '2')

    def test_sibling_after_deeper_level_does_not_inherit_stale_parent(self):
        # 1.2 (level 2) follows 1.1.1/1.1.2 (level 3) — its parent must
        # still resolve to "1", not linger on "1.1".
        by_ref_code = {c['refCode']: c for c in self.capabilities}
        self.assertEqual(by_ref_code['1.2']['parentRefCode'], '1')
