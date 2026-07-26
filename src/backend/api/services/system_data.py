import os
import requests as re

from api.models.cvi_systems import CVISystemModel

from utils.LocalC2Data import c2_is_configured, get_local_system_data


def get_system_data(system_id, component=None):
    if not c2_is_configured():
        # No C2: serve the seeded system definition instead.
        system_data = get_local_system_data(system_id)
        if system_data is None:
            raise ValueError(
                "No C2 configured and no local system data for "
                "'{}'".format(system_id))
    else:
        system_data = re.get(
            url='http://{}system/{}'.format(
                os.environ.get('C2_REST'),
                system_id)).json()
        CVISystemModel(
            data=system_data).is_valid(
            raise_exception=True)
        site_data = get_c2_site_data()
        if len(site_data) > 0:
            system_data['groups'] += get_site_group()
            system_data['assets'] += site_data
    if component in system_data.keys():
        return system_data[component]
    else:
        return system_data


def get_c2_site_data():
    data = re.get(
        url="http://{}missions/DPS-MISSION".format(
            os.environ.get('C2_REST'))).json()
    converted_sites = []
    if len(data["overlays"]) > 0:
        drawings = data["overlays"][0]["drawings"]
        for drawing in drawings:
            if "represents" in drawing and drawing["represents"]["entityType"] == "site":
                site = {
                    "id": drawing["represents"]["entityId"],
                    "function": "",
                    "assetType": "cyber",
                    "group": "Sites",
                    "name": drawing["label"],
                    "impact": {
                        "integrity": "3",
                        "confidentiality": "3",
                        "availability": "3",
                        "id": None
                    },
                    "sensitivity": 0
                }
                converted_sites.append(site)
    return converted_sites


def get_site_group():
    site_group = [{
        "id": "Sites",
        "name": "Sites",
        "description": "LayerType"
    }]
    return site_group
