from rest_framework import serializers

from api.models.effects import EFFECT_TYPES


class HostileResponsePairModel(serializers.Serializer):
    # Plain CharFields rather than ChoiceFields: users can create new effect
    # terms through the Actions page, so the set of valid names is open-ended.
    mostDangerous = serializers.CharField(required=True)
    mostLikely = serializers.CharField(required=True)


class HostileResponseModel(serializers.Serializer):
    effect = serializers.CharField(required=True)
    effectType = serializers.ChoiceField(
        choices=EFFECT_TYPES,
        required=True)
    description = serializers.CharField(
        required=True,
        allow_blank=True)
    hostileResponse = HostileResponsePairModel(required=True)
