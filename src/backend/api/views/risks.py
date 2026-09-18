import os
from datetime import date

import pymongo as pm
from bson import ObjectId
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateDestroyAPIView
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response

from analytics.Fair import annualized_loss_expectancy, residual_ale
from api.serializers.risks import RiskSerializer

MONGO_ID = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=False)

MONGO_ID_R = openapi.Parameter(
    name='_id', in_=openapi.IN_QUERY, description='A Mongo ID string',
    type=openapi.TYPE_STRING, required=True)

OVERDUE = openapi.Parameter(
    name='overdue', in_=openapi.IN_QUERY,
    description='If "true", only return open/in-progress risks whose reviewDate has passed',
    type=openapi.TYPE_STRING, required=False)


class RisksView(RetrieveUpdateDestroyAPIView):
    """
    CRUD over risks. Risk Assessment (F5) writes the FAIR inputs; Risk
    Register (F10, F11) manages the lifecycle fields — both against the same
    document, per the requirements' Key Decision.
    """
    renderer_classes = (JSONRenderer,)
    serializer_class = RiskSerializer

    def __init__(self):
        database = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]
        self.risks_collection = database['risks']
        self.controls_collection = database['controls']

    @swagger_auto_schema(manual_parameters=[MONGO_ID, OVERDUE])
    def get(self, request, *args, **kwargs):
        query_params = dict(self.request.GET.items())
        overdue_only = query_params.pop('overdue', 'false').lower() == 'true'
        if '_id' in query_params:
            query_params['_id'] = ObjectId(query_params['_id'])
        risks = list(self.risks_collection.find(query_params))
        if overdue_only:
            today = date.today().isoformat()
            risks = [
                risk for risk in risks
                if risk.get('status') != 'closed'
                and risk.get('reviewDate')
                and risk['reviewDate'] < today
            ]
        for risk in risks:
            risk['_id'] = str(risk['_id'])
        return Response(data=risks, status=200)

    def post(self, request, *args, **kwargs):
        RiskSerializer(data=request.data).is_valid(raise_exception=True)
        risk = dict(request.data)
        self._score(risk)
        result = self.risks_collection.insert_one(risk)
        return Response(
            data={
                '_id': str(result.inserted_id),
                'inherentAle': risk['inherentAle'],
                'residualAle': risk['residualAle'],
            },
            status=201)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def patch(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        existing = self.risks_collection.find_one({'_id': ObjectId(mongo_id)}) or {}
        update_fields = dict(existing)
        update_fields.update(dict(request.data))
        update_fields.pop('_id', None)
        self._score(update_fields)
        self.risks_collection.update_one(
            {'_id': ObjectId(mongo_id)},
            {"$set": update_fields},
            upsert=False)
        return Response(
            data={
                'inherentAle': update_fields['inherentAle'],
                'residualAle': update_fields['residualAle'],
            },
            status=200)

    @swagger_auto_schema(manual_parameters=[MONGO_ID_R])
    def delete(self, request, *args, **kwargs):
        mongo_id = self.request.GET.get('_id', None)
        if mongo_id is None:
            raise ValueError("Please provide a Mongo ID as query parameter (_id)")
        self.risks_collection.delete_one({'_id': ObjectId(mongo_id)})
        return Response(status=204)

    def _score(self, risk):
        """Recompute inherent/residual ALE from the risk's current FAIR inputs and mapped controls."""
        inherent = annualized_loss_expectancy(risk.get('lef'), risk.get('lm'))
        mapped_controls = list(self.controls_collection.find({
            '$or': [
                {'attackTechniqueIds': {'$in': risk.get('attackTechniqueIds', [])}},
                {'assetIds': {'$in': risk.get('assetIds', [])}},
            ]
        })) if (risk.get('attackTechniqueIds') or risk.get('assetIds')) else []
        risk['inherentAle'] = inherent
        risk['residualAle'] = residual_ale(inherent, mapped_controls)
