import os

import pymongo as pm
from bson import ObjectId
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from analytics.Fair import capability_rollup
from api.serializers.capabilities import CapabilitySerializer

MONGO_ID = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=False)

MONGO_ID_R = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=True)

CAPABILITY_FILE = openapi.Parameter(
    name='file', in_=openapi.IN_FORM,
    description='A .docx using Heading 1-4 styles with numbered text (e.g. "1.2.3")',
    type=openapi.TYPE_FILE, required=True)


def _db():
    return pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT'))
    )[os.environ.get('DB_NAME')]


class CapabilitiesView(RetrieveUpdateDestroyAPIView):
    """CRUD + manual reorder (via PATCH) over the capability hierarchy (F12, F13)."""
    renderer_classes = (JSONRenderer,)
    serializer_class = CapabilitySerializer

    def __init__(self):
        self.capabilities_collection = _db()['capabilities']

    @swagger_auto_schema(manual_parameters=[MONGO_ID])
    def get(self, request, *args, **kwargs):
        query_params = dict(self.request.GET.items())
        if '_id' in query_params:
            query_params['_id'] = ObjectId(query_params['_id'])
        capabilities = list(
            self.capabilities_collection.find(query_params).sort([
                ('level', 1), ('order', 1)]))
        for capability in capabilities:
            capability['_id'] = str(capability['_id'])
        return Response(data=capabilities, status=200)

    def post(self, request, *args, **kwargs):
        CapabilitySerializer(data=request.data).is_valid(raise_exception=True)
        result = self.capabilities_collection.insert_one(dict(request.data))
        return Response(data={'_id': str(result.inserted_id)}, status=201)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def patch(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        update_fields = dict(request.data)
        update_fields.pop('_id', None)
        self.capabilities_collection.update_one(
            {'_id': ObjectId(mongo_id)},
            {"$set": update_fields},
            upsert=False)
        return Response(status=204)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def delete(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        self.capabilities_collection.delete_one({'_id': ObjectId(mongo_id)})
        return Response(status=204)


class CapabilityImportView(APIView):
    """One-time bulk import of the capability hierarchy from a Word document (F12)."""
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        self.capabilities_collection = _db()['capabilities']

    @swagger_auto_schema(manual_parameters=[CAPABILITY_FILE], responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        # Imported lazily: python-docx (and this whole import path) is only
        # needed for this one endpoint, not for every request the app serves.
        from utils.CapabilityImport import parse_capability_document

        uploaded_file = request.FILES.get('file')
        if uploaded_file is None:
            return Response(
                data={'detail': 'Please attach a .docx file as "file".'},
                status=400)
        capabilities = parse_capability_document(uploaded_file)
        if capabilities:
            self.capabilities_collection.insert_many(capabilities)
        return Response(data={'imported': len(capabilities)}, status=201)


class CapabilityRiskRollupView(APIView):
    """GET /capabilities/<id>/risk_rollup/ — F14 aggregated residual ALE."""
    renderer_classes = (JSONRenderer,)

    def __init__(self):
        database = _db()
        self.capabilities_collection = database['capabilities']
        self.assets_collection = database['itAssets']
        self.risks_collection = database['risks']

    def get(self, request, *args, **kwargs):
        capability_id = self.kwargs['capabilityId']
        assets = list(self.assets_collection.find(
            {'capabilityIds': capability_id}))
        asset_ids = [str(asset['_id']) for asset in assets]
        risks = list(self.risks_collection.find(
            {'assetIds': {'$in': asset_ids}})) if asset_ids else []
        return Response(
            data={
                'capabilityId': capability_id,
                'assetCount': len(assets),
                'riskCount': len(risks),
                'residualAle': capability_rollup(risks),
            },
            status=200)
