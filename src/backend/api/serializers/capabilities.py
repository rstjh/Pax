from rest_framework import serializers


class CapabilitySerializer(serializers.Serializer):
    """A node in the TOGAF-aligned business capability hierarchy (F12)."""
    refCode = serializers.CharField(required=True)
    level = serializers.IntegerField(min_value=1, max_value=4, required=True)
    name = serializers.CharField(required=True)
    description = serializers.CharField(required=False, allow_blank=True)
    parentRefCode = serializers.CharField(required=False, allow_null=True)
    order = serializers.IntegerField(required=False)
