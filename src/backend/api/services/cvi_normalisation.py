"""
Normalise CVI system definitions into the canonical shape.

System definitions arrive from three places that each encode things slightly
differently: the CVI questionnaire (numeric threat levels, no geolocation or
network questions), the bundled C2 sample response (capitalised asset types),
and Pax's own seed data (the canonical form). This module reconciles them so
`CVISystemModel` has a single shape to validate.
"""

# The CVI questionnaire stores threat level as a rating value; its labels are
# the vocabulary analytics.Config.threat_label_level_map understands.
THREAT_LEVEL_BY_RATING = {
    5: 'CRITICAL',
    4: 'SEVERE',
    3: 'SUBSTANTIAL',
    2: 'MODERATE',
    1: 'LOW',
    0: 'NEGLIGIBLE'
}

DEFAULT_GEOLOCATION = {
    'coordinates': {
        'latitude': 0,
        'longitude': 0
    }
}


def _slugify(name):
    return '-'.join(str(name).upper().split())


def normalise_cvi_system(data):
    """
    Return `data` with the variations above reconciled. Mutates and returns
    the mapping it is given.
    """
    if not isinstance(data, dict):
        return data

    if not data.get('id') and data.get('name'):
        data['id'] = _slugify(data['name'])

    # The questionnaire has no geolocation or network pages.
    if not data.get('geolocation'):
        data['geolocation'] = dict(DEFAULT_GEOLOCATION)
    if data.get('networks') is None:
        data['networks'] = []

    for asset in data.get('assets') or []:
        # The CVI questionnaire names this column 'type'; everywhere else it is
        # 'assetType'.
        if not asset.get('assetType') and asset.get('type'):
            asset['assetType'] = asset['type']
        if asset.get('assetType'):
            asset['assetType'] = str(asset['assetType']).lower()

    for threat in data.get('threats') or []:
        threat_level = threat.get('threatLevel')
        if isinstance(threat_level, bool):
            continue
        if isinstance(threat_level, int):
            threat['threatLevel'] = THREAT_LEVEL_BY_RATING.get(
                threat_level, 'MODERATE')
        elif threat_level:
            threat['threatLevel'] = str(threat_level).upper()

    return data
