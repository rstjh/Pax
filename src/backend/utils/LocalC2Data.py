"""
Fallback data source for when no external C2 system is configured.

Pax normally reads system and unit data from an external C2 REST API (env var
`C2_REST`). For standalone development and demos there is no C2 to talk to, so
these helpers serve the equivalent data out of the seeded Mongo collections
(`cviSystems`, `units`) instead, letting the risk analysis run end to end.

When `C2_REST` is set the C2 remains the source of truth and none of this is used.
"""

import os

import pymongo as pm


def c2_is_configured():
    return bool(os.environ.get('C2_REST'))


def _database():
    client = pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT')))
    return client[os.environ.get('DB_NAME')]


def get_local_system_data(system_id):
    """
    The local stand-in for GET {C2_REST}/system/{system_id}.
    Returns None when the system is not in the seeded data.
    """
    return _database()['cviSystems'].find_one(
        {'id': system_id},
        {'_id': 0})


def get_local_units():
    """The local stand-in for GET {C2_REST}entity/Unit/."""
    return list(_database()['units'].find({}, {'_id': 0}))


def get_local_unit(unit_id):
    """The local stand-in for GET {C2_REST}entity/Unit/{unit_id}."""
    return _database()['units'].find_one(
        {'id': unit_id},
        {'_id': 0})
