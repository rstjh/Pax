import json

import pymongo as pm

from utils import SystemConfig as config
from utils.data.ActionListData import default_action_list
from utils.data.ActionTemplateData import default_action_templates
from utils.data.AttackData import default_attack_tactics, default_attack_techniques
from utils.data.CVISystemData import default_cvi_systems
from utils.data.EffectData import default_effects
from utils.data.HostileResponseData import default_hostile_responses
from utils.data.MissionData import default_missions
from utils.data.NetworkData import default_device_network
from utils.data.RiskAppetite import default_risk_appetite
from utils.data.UnitData import default_units

CLIENT = pm.MongoClient(
    host=config.DB_HOSTNAME,
    port=config.DB_PORT)


def reset_app_data():
    coll_data = {
        'effects': default_effects,
        'hostile_response': default_hostile_responses,
        'action_list': default_action_list,
        'actionTemplates': default_action_templates,
        'cviSystems': default_cvi_systems,
        'deviceNetwork': default_device_network,
        'riskAppetite': default_risk_appetite,
        'missions': default_missions,
        'units': default_units,
        'actionInstances': None
    }
    for coll, data in coll_data.items():
        reset_mongo_data(
            collection=coll,
            mongo_data=data)


def seed_reference_data():
    """
    Idempotently seed reference/lookup data for the Defender Risk & Control
    Roadmap Tool. Unlike `reset_app_data()`, this never drops anything — it
    only inserts into a collection that is currently empty — because the
    tool's own register collections (capabilities, itAssets, controls,
    risks, roadmapPlan) hold data the team manually enters and must survive
    every server restart/autoreload, not just demo seed data.
    """
    seed_if_empty('attackTactics', default_attack_tactics)
    seed_if_empty('attackTechniques', default_attack_techniques)


def seed_if_empty(collection, mongo_data):
    coll = CLIENT[config.DB_NAME][collection]
    if mongo_data and coll.count_documents({}) == 0:
        coll.insert_many(mongo_data)


def load_task_data(path):
    return_data = []
    data = json.load(open(path))
    for CoAKey, CoAData in data.items():
        for element in CoAData:
            d = {
                "taskId": element["name"],
                "objective": element["objective"]["entityId"],
                "dependencies": element["dependencies"],
                "systemId": "POWER-STATION",
                "timeFrame": element["end"] - element["start"],
                "courseOfAction": CoAKey,
                "effect": element["effect"],
                "unit": element["assignee"]["entityId"]
            }
            return_data.append(d)
    return return_data


def load_course_action_data(data):
    coa_collection = CLIENT[config.DB_NAME]['courses_of_action']
    coa_collection.drop()

    coas = []
    for task in data:
        coas.append(task['courseOfAction'])
    coas = list(set(coas))

    for coa in coas:
        coa_collection.insert_one({
            'systemId': "POWER-STATION",
            'name': coa
        })


def reset_mongo_data(collection, mongo_data=None):
    coll = CLIENT[config.DB_NAME][collection]
    coll.drop()
    if mongo_data:
        coll.insert_many(mongo_data)
