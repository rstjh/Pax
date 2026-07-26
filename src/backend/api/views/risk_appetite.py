import os
import pymongo as pm

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from drf_yasg.utils import swagger_auto_schema

from analytics.RiskAppetite import RiskAppetiteAnalysis
from api.serializers.risk_appetite import RiskAppetiteSerializer


def score_risk_appetite(risk_appetite_data):
    """
    Score a completed risk appetite questionnaire, returning it annotated with
    the resulting score and label.
    """
    analysis = RiskAppetiteAnalysis(
        risk_appetite_data=risk_appetite_data)
    risk_appetite_score = analysis.generate_risk_appetite_score()
    risk_appetite_data.update({
        'riskAppetiteScore': risk_appetite_score,
        'riskAppetiteLabel': analysis.generate_risk_appetite_label(
            riskAppetiteScore=risk_appetite_score)
    })
    return risk_appetite_data


class RiskAppetiteView(ListCreateAPIView):
    """
    Collection-level risk appetite. The questionnaire is filled in without a
    mission context, so submissions POST here rather than to the per-mission
    detail route.
    """
    renderer_classes = (JSONRenderer,)
    serializer_class = RiskAppetiteSerializer

    def __init__(self):
        self.risk_appetite_collection = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]['riskAppetite']

    def get(self, request, *args, **kwargs):
        return Response(
            data=list(self.risk_appetite_collection.find({}, {'_id': 0})),
            status=200)

    # Implement the get_queryset to stop warnings of schema generation
    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        try:
            risk_appetite_data = score_risk_appetite(request.data)
        except ValueError as unscoreable:
            # The questionnaire answered none of the questions the appetite is
            # derived from: a bad submission, not a server fault.
            return Response(
                data={'detail': str(unscoreable)},
                status=400)
        self.risk_appetite_collection.insert_one(dict(risk_appetite_data))
        # Returned so the questionnaire can display the resulting appetite.
        return Response(
            data={
                'riskAppetiteScore': risk_appetite_data['riskAppetiteScore'],
                'riskAppetiteLabel': risk_appetite_data['riskAppetiteLabel']
            },
            status=201)


class RiskAppetiteDetail(RetrieveUpdateDestroyAPIView):
    renderer_classes = (JSONRenderer,)
    serializer_class = RiskAppetiteSerializer

    def __init__(self):
        self.risk_appetite_collection = pm.MongoClient(
            host=os.environ.get('DB_HOSTNAME'),
            port=int(os.environ.get('DB_PORT'))
        )[os.environ.get('DB_NAME')]['riskAppetite']

    def get(self, request, *args, **kwargs):
        mission_id = self.kwargs['missionId']
        risk_appetite_data = list(self.risk_appetite_collection.find(
            {'missionId': mission_id},
            {'_id': 0}))
        return Response(
            data=risk_appetite_data,
            status=200)

    def put(self, request, *args, **kwargs):
        risk_appetite_data = score_risk_appetite(request.data)
        risk_appetite_data['missionId'] = self.kwargs['missionId']
        self.risk_appetite_collection.insert_one(dict(risk_appetite_data))
        return Response(status=201)

    def patch(self, request, *args, **kwargs):
        self.risk_appetite_collection.update({
            'missionId': self.kwargs['missionId']},
            {"$set": request.data},
            upsert=False)
        return Response(data=204)

    def delete(self, request, *args, **kwargs):
        self.risk_appetite_collection.delete_one({
            'missionId': self.kwargs['missionId']})
        return Response(status=204)
