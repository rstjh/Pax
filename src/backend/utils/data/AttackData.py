"""
Starter MITRE ATT&CK reference data for the Coverage Matrix (F3, F4).

This is a curated *starting point*, not a full mirror of MITRE's published
dataset — hand-typing the complete Enterprise (~200 techniques) and ICS
(~80 techniques) matrices from memory risks silent inaccuracies in a
security-relevant reference set. Per the requirements' Key Decision
("ATT&CK framework updates... handled manually"), the intended workflow is:

  1. Ship with this starting set so the Coverage Matrix is usable immediately.
  2. The team loads MITRE's authoritative, currently-published Enterprise +
     ICS STIX/JSON data through `POST /attack_reference/import/`
     (see api/views/attack_reference.py) to replace/extend it whenever
     convenient — matching the "no automated sync" decision.

Tactic names and their 14 Enterprise / 12 ICS structure are stable,
well-documented framework facts and can be trusted; the *technique* lists
below are a genuinely useful but deliberately partial starting set — only
techniques whose id/name pairing is well-established are included. ICS
technique IDs are omitted here entirely (left to the importer) rather than
risk shipping a fabricated-looking ID as fact.
"""

# The 14 MITRE ATT&CK Enterprise tactics, in kill-chain order.
default_attack_tactics = [
    {'id': 'TA0043', 'name': 'Reconnaissance', 'matrix': 'enterprise'},
    {'id': 'TA0042', 'name': 'Resource Development', 'matrix': 'enterprise'},
    {'id': 'TA0001', 'name': 'Initial Access', 'matrix': 'enterprise'},
    {'id': 'TA0002', 'name': 'Execution', 'matrix': 'enterprise'},
    {'id': 'TA0003', 'name': 'Persistence', 'matrix': 'enterprise'},
    {'id': 'TA0004', 'name': 'Privilege Escalation', 'matrix': 'enterprise'},
    {'id': 'TA0005', 'name': 'Defense Evasion', 'matrix': 'enterprise'},
    {'id': 'TA0006', 'name': 'Credential Access', 'matrix': 'enterprise'},
    {'id': 'TA0007', 'name': 'Discovery', 'matrix': 'enterprise'},
    {'id': 'TA0008', 'name': 'Lateral Movement', 'matrix': 'enterprise'},
    {'id': 'TA0009', 'name': 'Collection', 'matrix': 'enterprise'},
    {'id': 'TA0011', 'name': 'Command and Control', 'matrix': 'enterprise'},
    {'id': 'TA0010', 'name': 'Exfiltration', 'matrix': 'enterprise'},
    {'id': 'TA0040', 'name': 'Impact', 'matrix': 'enterprise'},

    # The 12 MITRE ATT&CK for ICS tactics. IDs are intentionally left blank
    # (see module docstring) — populate via the importer.
    {'id': 'ICS-INITIAL-ACCESS', 'name': 'Initial Access', 'matrix': 'ics'},
    {'id': 'ICS-EXECUTION', 'name': 'Execution', 'matrix': 'ics'},
    {'id': 'ICS-PERSISTENCE', 'name': 'Persistence', 'matrix': 'ics'},
    {'id': 'ICS-PRIVILEGE-ESCALATION', 'name': 'Privilege Escalation', 'matrix': 'ics'},
    {'id': 'ICS-EVASION', 'name': 'Evasion', 'matrix': 'ics'},
    {'id': 'ICS-DISCOVERY', 'name': 'Discovery', 'matrix': 'ics'},
    {'id': 'ICS-LATERAL-MOVEMENT', 'name': 'Lateral Movement', 'matrix': 'ics'},
    {'id': 'ICS-COLLECTION', 'name': 'Collection', 'matrix': 'ics'},
    {'id': 'ICS-COMMAND-AND-CONTROL', 'name': 'Command and Control', 'matrix': 'ics'},
    {'id': 'ICS-INHIBIT-RESPONSE-FUNCTION', 'name': 'Inhibit Response Function', 'matrix': 'ics'},
    {'id': 'ICS-IMPAIR-PROCESS-CONTROL', 'name': 'Impair Process Control', 'matrix': 'ics'},
    {'id': 'ICS-IMPACT', 'name': 'Impact', 'matrix': 'ics'},
]

# A partial, well-known set of Enterprise techniques per tactic — enough to
# exercise the Coverage Matrix meaningfully. Not exhaustive; refresh via the
# importer for full coverage.
default_attack_techniques = [
    {'id': 'T1595', 'name': 'Active Scanning', 'matrix': 'enterprise', 'tacticIds': ['TA0043']},
    {'id': 'T1589', 'name': 'Gather Victim Identity Information', 'matrix': 'enterprise', 'tacticIds': ['TA0043']},

    {'id': 'T1583', 'name': 'Acquire Infrastructure', 'matrix': 'enterprise', 'tacticIds': ['TA0042']},
    {'id': 'T1587', 'name': 'Develop Capabilities', 'matrix': 'enterprise', 'tacticIds': ['TA0042']},

    {'id': 'T1566', 'name': 'Phishing', 'matrix': 'enterprise', 'tacticIds': ['TA0001']},
    {'id': 'T1190', 'name': 'Exploit Public-Facing Application', 'matrix': 'enterprise', 'tacticIds': ['TA0001']},
    {'id': 'T1078', 'name': 'Valid Accounts', 'matrix': 'enterprise', 'tacticIds': ['TA0001', 'TA0003', 'TA0004', 'TA0005']},

    {'id': 'T1059', 'name': 'Command and Scripting Interpreter', 'matrix': 'enterprise', 'tacticIds': ['TA0002']},
    {'id': 'T1204', 'name': 'User Execution', 'matrix': 'enterprise', 'tacticIds': ['TA0002']},
    {'id': 'T1203', 'name': 'Exploitation for Client Execution', 'matrix': 'enterprise', 'tacticIds': ['TA0002']},

    {'id': 'T1053', 'name': 'Scheduled Task/Job', 'matrix': 'enterprise', 'tacticIds': ['TA0003', 'TA0004']},
    {'id': 'T1547', 'name': 'Boot or Logon Autostart Execution', 'matrix': 'enterprise', 'tacticIds': ['TA0003', 'TA0004']},

    {'id': 'T1055', 'name': 'Process Injection', 'matrix': 'enterprise', 'tacticIds': ['TA0004', 'TA0005']},

    {'id': 'T1027', 'name': 'Obfuscated Files or Information', 'matrix': 'enterprise', 'tacticIds': ['TA0005']},
    {'id': 'T1070', 'name': 'Indicator Removal', 'matrix': 'enterprise', 'tacticIds': ['TA0005']},

    {'id': 'T1110', 'name': 'Brute Force', 'matrix': 'enterprise', 'tacticIds': ['TA0006']},
    {'id': 'T1003', 'name': 'OS Credential Dumping', 'matrix': 'enterprise', 'tacticIds': ['TA0006']},
    {'id': 'T1556', 'name': 'Modify Authentication Process', 'matrix': 'enterprise', 'tacticIds': ['TA0006']},

    {'id': 'T1082', 'name': 'System Information Discovery', 'matrix': 'enterprise', 'tacticIds': ['TA0007']},
    {'id': 'T1087', 'name': 'Account Discovery', 'matrix': 'enterprise', 'tacticIds': ['TA0007']},
    {'id': 'T1046', 'name': 'Network Service Discovery', 'matrix': 'enterprise', 'tacticIds': ['TA0007']},

    {'id': 'T1021', 'name': 'Remote Services', 'matrix': 'enterprise', 'tacticIds': ['TA0008']},
    {'id': 'T1550', 'name': 'Use Alternate Authentication Material', 'matrix': 'enterprise', 'tacticIds': ['TA0008']},

    {'id': 'T1005', 'name': 'Data from Local System', 'matrix': 'enterprise', 'tacticIds': ['TA0009']},
    {'id': 'T1114', 'name': 'Email Collection', 'matrix': 'enterprise', 'tacticIds': ['TA0009']},

    {'id': 'T1071', 'name': 'Application Layer Protocol', 'matrix': 'enterprise', 'tacticIds': ['TA0011']},
    {'id': 'T1105', 'name': 'Ingress Tool Transfer', 'matrix': 'enterprise', 'tacticIds': ['TA0011']},

    {'id': 'T1041', 'name': 'Exfiltration Over C2 Channel', 'matrix': 'enterprise', 'tacticIds': ['TA0010']},
    {'id': 'T1567', 'name': 'Exfiltration Over Web Service', 'matrix': 'enterprise', 'tacticIds': ['TA0010']},

    {'id': 'T1486', 'name': 'Data Encrypted for Impact', 'matrix': 'enterprise', 'tacticIds': ['TA0040']},
    {'id': 'T1490', 'name': 'Inhibit System Recovery', 'matrix': 'enterprise', 'tacticIds': ['TA0040']},
    {'id': 'T1498', 'name': 'Network Denial of Service', 'matrix': 'enterprise', 'tacticIds': ['TA0040']},
]
