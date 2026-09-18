"""
FAIR-style (Factor Analysis of Information Risk) quantitative risk scoring.

Phase 1 keeps the FAIR inputs deliberately simple: a single expert-judgement
estimate for Loss Event Frequency (LEF, occurrences/year) and Loss Magnitude
(LM, $ per occurrence) per risk, rather than the full FAIR probability
distributions. Industry benchmark data sourcing (DBIR, insurance data, etc.)
is out of scope for Phase 1 per the requirements' Key Decisions.
"""


def annualized_loss_expectancy(lef, lm):
    """
    ALE = Loss Event Frequency x Loss Magnitude — the standard FAIR
    single-loss expectation rolled up to an annual figure.
    """
    return float(lef or 0) * float(lm or 0)


def control_coverage(controls):
    """
    The combined effectiveness of a set of mapped controls, 0 (no coverage)
    to 1 (fully mitigated). Controls acting on the same risk are treated as
    independent safeguards, so their *failure* probabilities multiply:
    coverage = 1 - product(1 - effectiveness) across mapped, implemented
    controls. An empty or all-unimplemented set has no coverage.
    """
    residual_probability = 1.0
    for control in controls:
        if control.get('status') != 'Implemented':
            continue
        effectiveness = max(0.0, min(1.0, float(control.get('effectiveness', 0) or 0)))
        residual_probability *= (1.0 - effectiveness)
    return 1.0 - residual_probability


def residual_ale(inherent_ale, controls):
    """Residual ALE after applying the combined effectiveness of mapped controls."""
    return inherent_ale * (1.0 - control_coverage(controls))


def capability_rollup(risks):
    """
    Aggregate a capability's supporting assets' open risks into a single
    capability-level figure, per the requirements' Key Decision: "FAIR-based
    aggregation — combine loss frequency/magnitude... rather than simple
    average/max." Expected annual loss is additive across independent loss
    events, so the rollup is the sum of residual ALE across open risks.
    """
    return sum(
        float(risk.get('residualAle', 0) or 0)
        for risk in risks
        if risk.get('status') != 'closed')


def roadmap_roi(control, addressed_risks):
    """
    Rank candidate controls by ROI: the ALE reduction they would achieve
    across the risks they're mapped to, divided by their implementation
    cost. A zero/near-zero cost control is treated as maximally attractive
    rather than dividing by zero.
    """
    cost = float(control.get('cost', 0) or 0)
    effectiveness = max(0.0, min(1.0, float(control.get('effectiveness', 0) or 0)))
    risk_reduction = sum(
        float(risk.get('inherentAle', 0) or 0) * effectiveness
        for risk in addressed_risks
        if risk.get('status') != 'closed')
    if cost <= 0:
        return risk_reduction if risk_reduction > 0 else 0.0
    return risk_reduction / cost
