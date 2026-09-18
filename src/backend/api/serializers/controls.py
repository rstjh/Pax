from rest_framework import serializers

STATUS_CHOICES = ('Planned', 'In Progress', 'Implemented', 'Retired')


class ControlSerializer(serializers.Serializer):
    """An existing/planned control in the Control Register (F2)."""
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    owner = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(choices=STATUS_CHOICES, required=False, default='Planned')
    assetIds = serializers.ListField(
        child=serializers.CharField(), required=False, default=list)
    attackTechniqueIds = serializers.ListField(
        child=serializers.CharField(), required=False, default=list)
    # Implementation cost, used as the denominator of the roadmap ROI ranking.
    cost = serializers.FloatField(min_value=0, required=False, default=0)
    # How strongly this control reduces the likelihood/impact of the
    # techniques it mitigates, 0 (no effect) - 1 (fully mitigates).
    effectiveness = serializers.FloatField(min_value=0, max_value=1, required=False, default=0.5)
