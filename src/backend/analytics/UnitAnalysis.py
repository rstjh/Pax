import os
import requests

from utils.LocalC2Data import c2_is_configured, get_local_unit, get_local_units


def get_unit_data(unit_id):
    if not c2_is_configured():
        return get_local_unit(unit_id)
    r = requests.get('http://' + os.environ.get('C2_REST') + 'entity/Unit/' + unit_id)
    unit_data = r.json()
    return unit_data


def get_hostile_unit():
    if c2_is_configured():
        r = requests.get('http://' + os.environ.get('C2_REST') + 'entity/Unit/')
        unit_data = r.json()
    else:
        unit_data = get_local_units()
    hostile_units = [
        unit for unit in unit_data if unit['affiliation'] == 'HOSTILE'
    ]
    hostile_unit = hostile_units[0]
    return hostile_unit
