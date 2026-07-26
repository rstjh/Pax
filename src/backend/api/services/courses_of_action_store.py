"""
Local storage for courses of action.

Courses of action and their tasks are normally owned by the external C2 system
and reached over its `coa/mission/{missionId}/coa/...` routes. Pax has no C2 to
talk to, so they are stored here in the `coursesOfAction` collection and served
back on the mission object in the same shape the C2 supplied:

    {'id': ..., 'name': 'COA1', 'tasks': [{'id': ..., 'effect': ..., ...}]}
"""

import os
import uuid

import pymongo as pm


def _collection():
    client = pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT')))
    return client[os.environ.get('DB_NAME')]['coursesOfAction']


def _new_id():
    return uuid.uuid4().hex


def get_courses_of_action(mission_id):
    return list(_collection().find(
        {'missionId': mission_id},
        {'_id': 0, 'missionId': 0}))


def attach_courses_of_action(mission):
    """Add the mission's stored courses of action to it, as the C2 would."""
    mission['coAs'] = get_courses_of_action(mission['id'])
    return mission


def create_course_of_action(mission_id, name):
    course_of_action = {
        'missionId': mission_id,
        'id': _new_id(),
        'name': name,
        'tasks': []
    }
    _collection().insert_one(dict(course_of_action))
    course_of_action.pop('missionId', None)
    course_of_action.pop('_id', None)
    return course_of_action


def delete_course_of_action(mission_id, coa_id):
    result = _collection().delete_one({
        'missionId': mission_id,
        'id': coa_id})
    return result.deleted_count > 0


def add_task(mission_id, coa_id, task):
    task = dict(task)
    task.setdefault('id', _new_id())
    task.setdefault('dependencies', [])
    result = _collection().update_one(
        {'missionId': mission_id, 'id': coa_id},
        {'$push': {'tasks': task}})
    if result.matched_count == 0:
        return None
    return task


def delete_task(mission_id, coa_id, task_id):
    result = _collection().update_one(
        {'missionId': mission_id, 'id': coa_id},
        {'$pull': {'tasks': {'id': task_id}}})
    return result.matched_count > 0
