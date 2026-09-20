import os

import pymongo as pm
from bson import ObjectId
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.Fair import roadmap_roi
from api.serializers.roadmap import RoadmapPlanEntrySerializer

MONGO_ID_R = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=True)


def _db():
    return pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT'))
    )[os.environ.get('DB_NAME')]


class RoadmapCandidatesView(APIView):
    """
    GET /roadmap/candidates/ — not-yet-implemented controls ranked by ROI
    (ALE reduction across the risks they mitigate, divided by cost). F6.
    Computed live, not persisted — see RoadmapPlanView for the sequenced plan.
    """
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        database = _db()
        self.controls_collection = database['controls']
        self.risks_collection = database['risks']

    def get(self, request, *args, **kwargs):
        controls = list(self.controls_collection.find({'status': {'$ne': 'Implemented'}}))
        risks = list(self.risks_collection.find({'status': {'$ne': 'closed'}}))

        candidates = []
        for control in controls:
            control_id = str(control['_id'])
            addressed_risks = [
                risk for risk in risks
                if set(risk.get('attackTechniqueIds', [])) & set(control.get('attackTechniqueIds', []))
                or set(risk.get('assetIds', [])) & set(control.get('assetIds', []))
            ]
            candidates.append({
                'controlId': control_id,
                'name': control.get('name'),
                'cost': control.get('cost', 0),
                'status': control.get('status'),
                'addressedRiskCount': len(addressed_risks),
                'roi': roadmap_roi(control, addressed_risks),
            })
        candidates.sort(key=lambda candidate: candidate['roi'], reverse=True)
        return Response(data=candidates, status=200)


class RoadmapPlanView(RetrieveUpdateDestroyAPIView):
    """CRUD over the persisted, sequenced roadmap plan (F7)."""
    renderer_classes = (JSONRenderer,)
    serializer_class = RoadmapPlanEntrySerializer

    def __init__(self):
        self.roadmap_collection = _db()['roadmapPlan']

    def get(self, request, *args, **kwargs):
        entries = list(self.roadmap_collection.find({}).sort('quarter', 1))
        for entry in entries:
            entry['_id'] = str(entry['_id'])
        return Response(data=entries, status=200)

    def post(self, request, *args, **kwargs):
        RoadmapPlanEntrySerializer(data=request.data).is_valid(raise_exception=True)
        result = self.roadmap_collection.insert_one(dict(request.data))
        return Response(data={'_id': str(result.inserted_id)}, status=201)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def patch(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        update_fields = dict(request.data)
        update_fields.pop('_id', None)
        self.roadmap_collection.update_one(
            {'_id': ObjectId(mongo_id)},
            {"$set": update_fields},
            upsert=False)
        return Response(status=204)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def delete(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        self.roadmap_collection.delete_one({'_id': ObjectId(mongo_id)})
        return Response(status=204)
