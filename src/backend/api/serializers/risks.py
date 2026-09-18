from rest_framework import serializers

TREATMENT_CHOICES = ('mitigate', 'accept', 'transfer', 'avoid')
STATUS_CHOICES = ('open', 'in_progress', 'closed')


class RiskSerializer(serializers.Serializer):
    """
    A tracked risk: FAIR inputs/scores (Risk Assessment, F5) plus lifecycle
    fields (Risk Register, F10/F11) live on the same document (Key Decision:
    "Risk Register vs Risk Assessment... two separate pages" over one record).
    """
    title = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    owner = serializers.CharField(required=False, allow_blank=True)
    assetIds = serializers.ListField(
        child=serializers.CharField(), required=False, default=list)
    attackTechniqueIds = serializers.ListField(
        child=serializers.CharField(), required=False, default=list)

    # FAIR-style quantitative inputs, entered via expert judgement (F5).
    # lef = Loss Event Frequency (expected occurrences/year).
    # lm = Loss Magnitude (expected $ loss per occurrence).
    lef = serializers.FloatField(min_value=0, required=False)
    lm = serializers.FloatField(min_value=0, required=False)

    # Computed (not submitted) — see analytics.Fair.
    inherentAle = serializers.FloatField(required=False)
    residualAle = serializers.FloatField(required=False)

    # Risk Register lifecycle fields (F10, F11).
    treatment = serializers.ChoiceField(choices=TREATMENT_CHOICES, required=False)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False, default='open')
    reviewDate = serializers.DateField(required=False, allow_null=True)
