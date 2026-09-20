import os

import pymongo as pm
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from api.serializers.attack_reference import AttackReferenceImportSerializer

MATRIX = openapi.Parameter(
    name='matrix', in_=openapi.IN_QUERY,
    description='Filter to "enterprise" or "ics"',
    type=openapi.TYPE_STRING, required=False)


def _db():
    return pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT'))
    )[os.environ.get('DB_NAME')]


class AttackReferenceView(APIView):
    """GET /attack_reference/ — the seeded/imported tactic + technique reference data (F3)."""
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        database = _db()
        self.tactics_collection = database['attackTactics']
        self.techniques_collection = database['attackTechniques']

    @swagger_auto_schema(manual_parameters=[MATRIX])
    def get(self, request, *args, **kwargs):
        matrix = self.request.GET.get('matrix')
        tactic_filter = {'matrix': matrix} if matrix else {}
        tactics = list(self.tactics_collection.find(tactic_filter, {'_id': 0}))
        techniques = list(self.techniques_collection.find(tactic_filter, {'_id': 0}))
        return Response(data={'tactics': tactics, 'techniques': techniques}, status=200)


class AttackCoverageView(APIView):
    """
    GET /attack_reference/coverage/ — per-technique count of mapped,
    implemented controls, for the Coverage Matrix heatmap (F4).
    """
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        database = _db()
        self.techniques_collection = database['attackTechniques']
        self.controls_collection = database['controls']

    @swagger_auto_schema(manual_parameters=[MATRIX])
    def get(self, request, *args, **kwargs):
        matrix = self.request.GET.get('matrix')
        technique_filter = {'matrix': matrix} if matrix else {}
        techniques = list(self.techniques_collection.find(technique_filter, {'_id': 0}))
        controls = list(self.controls_collection.find({}, {'_id': 0, 'attackTechniqueIds': 1, 'status': 1}))

        coverage = []
        for technique in techniques:
            mapped = [
                control for control in controls
                if technique['id'] in control.get('attackTechniqueIds', [])
            ]
            coverage.append({
                'techniqueId': technique['id'],
                'techniqueName': technique['name'],
                'tacticIds': technique.get('tacticIds', []),
                'controlCount': len(mapped),
                'implementedControlCount': len(
                    [c for c in mapped if c.get('status') == 'Implemented']),
            })
        return Response(data=coverage, status=200)


class AttackReferenceImportView(APIView):
    """
    POST /attack_reference/import/ — load MITRE's authoritative published
    tactic/technique data, replacing entries with matching ids and adding
    new ones. Manual, on-demand — per the requirements' Key Decision that
    ATT&CK updates are handled manually, not auto-synced.
    """
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        database = _db()
        self.tactics_collection = database['attackTactics']
        self.techniques_collection = database['attackTechniques']

    def post(self, request, *args, **kwargs):
        AttackReferenceImportSerializer(data=request.data).is_valid(raise_exception=True)
        tactics = request.data.get('tactics', [])
        techniques = request.data.get('techniques', [])
        for tactic in tactics:
            self.tactics_collection.update_one(
                {'id': tactic['id']}, {"$set": tactic}, upsert=True)
        for technique in techniques:
            self.techniques_collection.update_one(
                {'id': technique['id']}, {"$set": technique}, upsert=True)
        return Response(
            data={'tacticsImported': len(tactics), 'techniquesImported': len(techniques)},
            status=201)
