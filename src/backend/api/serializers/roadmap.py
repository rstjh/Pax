from rest_framework import serializers

PLAN_STATUS_CHOICES = ('planned', 'in_progress', 'done')


class RoadmapPlanEntrySerializer(serializers.Serializer):
    """A persisted, sequenced roadmap entry (F7) for one candidate control."""
    controlId = serializers.CharField(required=True)
    quarter = serializers.CharField(required=True)  # e.g. "2026-Q4"
    rationale = serializers.CharField(required=False, allow_blank=True)
    status = serializers.ChoiceField(
        choices=PLAN_STATUS_CHOICES, required=False, default='planned')
