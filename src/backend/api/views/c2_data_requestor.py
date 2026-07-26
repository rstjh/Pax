import os
import json
import requests

from rest_framework.response import Response
from rest_framework_mongoengine.generics import CreateAPIView
from rest_framework.renderers import JSONRenderer

from api.models.cvi_systems import CVISystemModel

from api.services.system_data import get_system_data

from utils import SystemConfig as config
from utils.LocalC2Data import c2_is_configured, get_local_system_data


class C2DataRequestor(CreateAPIView):
    renderer_classes = (JSONRenderer,)

    def fetch_c2_data(self, request, system_id):
        if c2_is_configured():
            system_data = self.fetch_system_data_from_c2(system_id)
        else:
            # No C2 to talk to: fall back to the seeded local system data so
            # the risk analysis still runs standalone.
            system_data = get_local_system_data(system_id)
            if system_data is None:
                raise ValueError(
                    "No C2 configured and no local system data for "
                    "'{}'".format(system_id))

        return self.status_200(system_id, request, system_data)

    def fetch_system_data_from_c2(self, system_id):
        response = requests.get(
            url="http://{}/system/{}".format(
                os.environ.get('C2_REST'),
                system_id))

        if response.status_code == 200:
            CVISystemModel(
                data=response.json()
            ).is_valid(
                raise_exception=True)
        else:
            raise ValueError("Could not find system data from C2")

        return get_system_data(
            system_id=system_id)

    def missing_keys(self, missing_keys):
        context = {
            "Message": "Missing the follow keys from C2 data request:",
            "MissingKeys": missing_keys
        }
        return Response(data=context, status=409)

    def c2_error(self, result):
        data = None

        try:
            data = result.json()
        except ValueError:
            pass

        context = {
            "Message": "There was an error from the c2 api",
            "c2_error_code": result.status_code,
            "c2_pay_load": data
        }
        return Response(data=context, status=400)
