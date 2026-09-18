from rest_framework import serializers

CRITICALITY_CHOICES = ('Low', 'Medium', 'High', 'Critical')

# "domain" future-proofs the asset register for Phase 2 (Physical) and
# Phase 3 (OT/ICS) per F9 / the requirements' Non-Functional Notes, even
# though only "IT" assets are entered through the UI in Phase 1.
DOMAIN_CHOICES = ('IT', 'Physical', 'OT')


class ITAssetSerializer(serializers.Serializer):
    """An asset in the Phase 1 IT Asset Register (F1)."""
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    owner = serializers.CharField(required=False, allow_blank=True)
    criticality = serializers.ChoiceField(choices=CRITICALITY_CHOICES, required=True)
    domain = serializers.ChoiceField(choices=DOMAIN_CHOICES, required=False, default='IT')
    capabilityIds = serializers.ListField(
        child=serializers.CharField(), required=False, default=list)
