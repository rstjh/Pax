import os
import pymongo as pm

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_yasg.utils import swagger_auto_schema

from api.models.cvi_systems import CVISystemModel
from api.services.cvi_normalisation import normalise_cvi_system


class CVIView(ListCreateAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = CVISystemModel

    def __init__(self):
        self.cvi_collection = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]['cviSystems']

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request, *args, **kwargs):
        cvi_systems_list = list(self.cvi_collection.find())
        for cvi_system in cvi_systems_list:
            cvi_system['_id'] = str(cvi_system['_id'])
        return Response(
            data=cvi_systems_list,
            status=200)

    # Fields the CVI questionnaire has no pages for. If it is updating a system
    # that already has them, they must be carried over rather than reset to
    # empty defaults.
    PRESERVED_FIELDS = ('geolocation', 'networks')

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        unanswered = [field for field in self.PRESERVED_FIELDS
                      if not request.data.get(field)]
        system_data = normalise_cvi_system(request.data)

        if unanswered:
            existing = self.cvi_collection.find_one(
                {'id': system_data['id']},
                {'_id': 0}) or {}
            for field in unanswered:
                if existing.get(field):
                    system_data[field] = existing[field]

        CVISystemModel(
            data=system_data).is_valid(
            raise_exception=True)
        # Keyed on the system id so re-submitting the questionnaire for a
        # system updates it rather than accumulating duplicates.
        self.cvi_collection.replace_one(
            {'id': system_data['id']},
            system_data,
            upsert=True)
        return Response(status=201)


class CVISystemView(RetrieveUpdateDestroyAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = CVISystemModel

    def __init__(self):
        self.cvi_collection = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]['cviSystems']

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request, *args, **kwargs):
        cvi_system = list(self.cvi_collection.find(
            {"id": self.kwargs['systemId']}))
        return Response(
            data=cvi_system,
            status=200)

    @swagger_auto_schema(responses={204: "No content"})
    def put(self, request, *args, **kwargs):
        CVISystemModel(
            data=request.data).is_valid(
            raise_exception=True)
        self.cvi_collection.update(
            {'id': self.kwargs['systemId']},
            {"$set": request.data},
            upsert=False)
        return Response(status=204)

    @swagger_auto_schema(responses={204: "No content"})
    def patch(self, request, *args, **kwargs):
        CVISystemModel(
            data=request.data).is_valid(
            raise_exception=True)
        self.cvi_collection.update(
            {'id': self.kwargs['systemId']},
            {"$set": request.data},
            upsert=False)
        return Response(status=204)

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, *args, **kwargs):
        self.action_instances_collection.delete_one(
            {'id': self.kwargs['systemId']})
        return Response(status=204)
