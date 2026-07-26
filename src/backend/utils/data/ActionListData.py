from utils.data.EffectData import default_effects


ASSET_TYPES = ('physical', 'cyber', 'actor')

DEFAULT_ACTIONS = {
    'physical': [
        'Deploy ground unit',
        'Establish physical perimeter',
    ],
    'cyber': [
        'Run network operation',
        'Deploy cyber payload',
    ],
    'actor': [
        'Task field operative',
        'Coordinate with allied actors',
    ],
}


def build_default_action_list():
    """
    Development defaults for the `action_list` collection, one document per
    (effect, asset type) for the hostile force. Consumed by the Actions page
    (tables of actions plus time/likeliness properties per effect) and by
    analytics.HostileResponses (get_counter_actions, get_effect_likeliness).
    """
    action_list = []
    for effect in default_effects:
        for asset_type in ASSET_TYPES:
            action_list.append({
                'force': 'hostile',
                'effect': effect['effect'],
                'type': asset_type,
                'actions': list(DEFAULT_ACTIONS[asset_type]),
                'properties': {
                    'time': 60,
                    'likeliness': 50
                }
            })
    return action_list


default_action_list = build_default_action_list()
