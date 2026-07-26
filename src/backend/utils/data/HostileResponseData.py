from utils.data.EffectData import default_effects


def build_default_hostile_responses():
    """
    The legacy `hostile_response` collection schema, derived from the richer
    `effects` seed data so the two stay in sync. The Actions page and
    analytics.HostileResponses.get_counter_effects both read this shape:
    {effect, effectType, description, hostileResponse: {mostLikely, mostDangerous}}
    """
    hostile_responses = []
    for effect in default_effects:
        hostile_responses.append({
            'effect': effect['effect'],
            'effectType': effect['type'],
            'description': effect['description'],
            'hostileResponse': dict(
                effect['assetType']['physical']['hostileResponses'])
        })
    return hostile_responses


default_hostile_responses = build_default_hostile_responses()
