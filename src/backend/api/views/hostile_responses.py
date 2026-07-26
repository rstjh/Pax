import os

import pymongo as pm

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView

from api.models.hostile_responses import HostileResponseModel


PATCHABLE_FIELDS = ('effectType', 'description', 'hostileResponse')


def hostile_response_collection():
    client = pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT')))
    return client[os.environ.get('DB_NAME')]['hostile_response']


class HostileResponsesView(ListCreateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = HostileResponseModel

    def __init__(self):
        self.collection = hostile_response_collection()

    def get(self, request, *args, **kwargs):
        responses = list(self.collection.find({}, {'_id': 0}))
        return Response(
            data=responses,
            status=200)

    # Implement the get_queryset to stop warnings of schema generation
    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={201: ""})
    def post(self, request, *args, **kwargs):
        HostileResponseModel(
            data=request.data).is_valid(
            raise_exception=True)
        # Upsert keyed on the effect name so re-submitting an existing effect
        # updates it instead of accumulating duplicate documents.
        self.collection.replace_one(
            {'effect': request.data['effect']},
            request.data,
            upsert=True)
        return Response(status=201)


class HostileResponseDetailView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = HostileResponseModel

    def __init__(self):
        self.collection = hostile_response_collection()

    def get(self, request, *args, **kwargs):
        effect = self.kwargs['effect']
        responses = list(self.collection.find(
            {'effect': effect},
            {'_id': 0}))
        return Response(
            data=responses,
            status=200)

    # Implement the get_queryset to stop warnings of schema generation
    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={204: ""})
    def patch(self, request, *args, **kwargs):
        effect = self.kwargs['effect']
        update = {field: request.data[field]
                  for field in PATCHABLE_FIELDS
                  if field in request.data}
        if not update:
            return Response(
                data={'detail': 'No updatable fields supplied.'},
                status=400)
        self.collection.update_one(
            {'effect': effect},
            {'$set': update},
            upsert=False)
        return Response(status=204)

    def delete(self, request, *args, **kwargs):
        effect = self.kwargs['effect']
        self.collection.delete_many({'effect': effect})
        return Response(status=204)
