from unittest import TestCase

from analytics import Fair


class TestAnnualizedLossExpectancy(TestCase):

    def test_multiplies_frequency_by_magnitude(self):
        self.assertEqual(Fair.annualized_loss_expectancy(2, 500000), 1000000.0)

    def test_missing_inputs_default_to_zero(self):
        self.assertEqual(Fair.annualized_loss_expectancy(None, None), 0.0)


class TestControlCoverage(TestCase):

    def test_no_controls_gives_no_coverage(self):
        self.assertEqual(Fair.control_coverage([]), 0.0)

    def test_unimplemented_control_gives_no_coverage(self):
        controls = [{'status': 'Planned', 'effectiveness': 0.9}]
        self.assertEqual(Fair.control_coverage(controls), 0.0)

    def test_single_implemented_control(self):
        controls = [{'status': 'Implemented', 'effectiveness': 0.7}]
        self.assertAlmostEqual(Fair.control_coverage(controls), 0.7)

    def test_independent_controls_combine_by_failure_probability(self):
        # Two 50%-effective controls: neither stops it alone 50% of the
        # time, so both fail together 25% of the time -> 75% coverage.
        controls = [
            {'status': 'Implemented', 'effectiveness': 0.5},
            {'status': 'Implemented', 'effectiveness': 0.5},
        ]
        self.assertAlmostEqual(Fair.control_coverage(controls), 0.75)


class TestResidualAle(TestCase):

    def test_applies_combined_control_coverage(self):
        controls = [{'status': 'Implemented', 'effectiveness': 0.7}]
        self.assertAlmostEqual(Fair.residual_ale(1000000.0, controls), 300000.0)

    def test_no_controls_leaves_ale_unchanged(self):
        self.assertEqual(Fair.residual_ale(1000000.0, []), 1000000.0)


class TestCapabilityRollup(TestCase):

    def test_sums_residual_ale_of_open_risks(self):
        risks = [
            {'residualAle': 100000.0, 'status': 'open'},
            {'residualAle': 50000.0, 'status': 'in_progress'},
        ]
        self.assertEqual(Fair.capability_rollup(risks), 150000.0)

    def test_excludes_closed_risks(self):
        risks = [
            {'residualAle': 100000.0, 'status': 'open'},
            {'residualAle': 999999.0, 'status': 'closed'},
        ]
        self.assertEqual(Fair.capability_rollup(risks), 100000.0)

    def test_empty_risk_list_is_zero(self):
        self.assertEqual(Fair.capability_rollup([]), 0.0)


class TestRoadmapRoi(TestCase):

    def test_ranks_by_risk_reduction_over_cost(self):
        control = {'cost': 5000, 'effectiveness': 0.7}
        risks = [{'inherentAle': 1000000.0, 'status': 'open'}]
        self.assertAlmostEqual(Fair.roadmap_roi(control, risks), 140.0)

    def test_excludes_closed_risks_from_reduction(self):
        control = {'cost': 5000, 'effectiveness': 0.7}
        risks = [{'inherentAle': 1000000.0, 'status': 'closed'}]
        self.assertEqual(Fair.roadmap_roi(control, risks), 0.0)

    def test_zero_cost_uses_raw_risk_reduction(self):
        control = {'cost': 0, 'effectiveness': 1.0}
        risks = [{'inherentAle': 42.0, 'status': 'open'}]
        self.assertEqual(Fair.roadmap_roi(control, risks), 42.0)
