import os

import pymongo as pm
from bson import ObjectId
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from api.serializers.it_assets import ITAssetSerializer

MONGO_ID = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=False)

MONGO_ID_R = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=True)


class ITAssetsView(RetrieveUpdateDestroyAPIView):
    """CRUD over the Phase 1 IT Asset Register (F1, F13)."""
    renderer_classes = (JSONRenderer,)
    serializer_class = ITAssetSerializer

    def __init__(self):
        self.assets_collection = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]['itAssets']

    @swagger_auto_schema(manual_parameters=[MONGO_ID])
    def get(self, request, *args, **kwargs):
        query_params = dict(self.request.GET.items())
        if '_id' in query_params:
            query_params['_id'] = ObjectId(query_params['_id'])
        assets = list(self.assets_collection.find(query_params))
        for asset in assets:
            asset['_id'] = str(asset['_id'])
        return Response(data=assets, status=200)

    def post(self, request, *args, **kwargs):
        ITAssetSerializer(data=request.data).is_valid(raise_exception=True)
        result = self.assets_collection.insert_one(dict(request.data))
        return Response(data={'_id': str(result.inserted_id)}, status=201)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def patch(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        update_fields = dict(request.data)
        update_fields.pop('_id', None)
        self.assets_collection.update_one(
            {'_id': ObjectId(mongo_id)},
            {"$set": update_fields},
            upsert=False)
        return Response(status=204)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def delete(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        self.assets_collection.delete_one({'_id': ObjectId(mongo_id)})
        return Response(status=204)
