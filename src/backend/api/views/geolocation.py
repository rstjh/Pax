import os

from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListAPIView

from analytics.Geolocation import get_asset_actor_distance, \
    calculate_actor_to_asset_time


class AssetActorDistance(ListAPIView):
    """
    Distance and travel time between an asset and an actor (unit), used when
    staging a task to judge whether the actor can reach the objective.
    """
    renderer_classes = (JSONRenderer,)

    # Implement the get_queryset to stop warnings of schema generation
    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request, *args, **kwargs):
        distance = get_asset_actor_distance(
            system_id=self.kwargs['systemId'],
            asset_id=self.kwargs['assetId'],
            actor_id=self.kwargs['actorId'])
        return Response(
            data={
                'distance': distance,
                'time': calculate_actor_to_asset_time(distance=distance)
            },
            status=200)
