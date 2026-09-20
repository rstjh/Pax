from rest_framework import serializers

MATRIX_CHOICES = ('enterprise', 'ics')


class AttackTacticSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    matrix = serializers.ChoiceField(choices=MATRIX_CHOICES, required=True)


class AttackTechniqueSerializer(serializers.Serializer):
    id = serializers.CharField(required=True)
    name = serializers.CharField(required=True)
    matrix = serializers.ChoiceField(choices=MATRIX_CHOICES, required=True)
    tacticIds = serializers.ListField(child=serializers.CharField(), required=True)
    description = serializers.CharField(required=False, allow_blank=True)


class AttackReferenceImportSerializer(serializers.Serializer):
    """Body shape accepted by POST /attack_reference/import/."""
    tactics = AttackTacticSerializer(many=True, required=False, default=list)
    techniques = AttackTechniqueSerializer(many=True, required=False, default=list)
