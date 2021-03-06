default_cvi_systems = [
    {
        "id": "POWER-STATION",
        "name": "Power station",
        "description": "Power Station surrounded by woods on edge of lake in Belanovia",
        "geolocation": {
            "coordinates": {
                "latitude": 52.92513,
                "longitude": -3.94619
            }
        },
        "groups": [{
            "id": "POWER-STATION-G1",
            "description": "The safety critical network controlling the power generation "
                           "process. The network includes the machinery used to control the "
                           "plant and all HMI interfaces.",
            "name": "Safety Critical Network"
        }, {
            "id": "POWER-STATION-G2",
            "description": "The enterprise network focusing on the Local Area network and the "
                           "interconnections with the Wide Area Network and Internet.",
            "name": "Enterprise Network"
        }, {
            "id": "POWER-STATION-G3",
            "description": "The buildings and surrounding physical controls of the Trawsfynydd Site.",
            "name": "Physical Location"
        }],
        "functions": [{
            "description": "Generate power for the surrounding population.  The plant has two "
                           "reactors each generating 235 MW of electricity.\n\nThe plant draws "
                           "water from the nearby lake for cooling.",
            "name": "Generate",
            "id": "POWER-STATION-F1"
        }, {
            "description": "Store power ready to be supplied when demanded by the surrounding "
                           "population across national grid.",
            "name": "Distribute",
            "id": "POWER-STATION-F2"
        }, {
            "description": "Maintain the operation of the plant via delivery of new fuel and "
                           "dispose of spent fuel.",
            "name": "Maintain",
            "id": "POWER-STATION-F3"
        }, {
            "description": "Maintain cyber and physical security of the plant to prevent accidents.",
            "name": "Safety and Security",
            "id": "POWER-STATION-F4"
        }],
        "assets": [{
            "id": "POWER-STATION-A1",
            "assetType": "physical",
            "description": "Houses reactor 1 and 2.",
            "name": "Reactor Building",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL1",
                "integrity": "4",
                "availability": "5"
            },
            "sensitivity": 5
        }, {
            "id": "POWER-STATION-A2",
            "assetType": "physical",
            "description": "Houses the Turbines that generates the steam.",
            "name": "Turbine Building",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL2",
                "integrity": "4",
                "availability": "5"
            },
            "sensitivity": 4
        }, {
            "id": "POWER-STATION-A3",
            "assetType": "physical",
            "description": "Houses the pumps that moves the coolant water around.",
            "name": "Pump Building",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL3",
                "integrity": "4",
                "availability": "5"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-A4",
            "assetType": "physical",
            "description": "This is the building that houses the switches to supply or received "
                           "power from the electricity grid.",
            "name": "Switch Compound",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL4",
                "integrity": "4",
                "availability": "5"
            },
            "sensitivity": 2
        }, {
            "id": "POWER-STATION-A5",
            "assetType": "physical",
            "description": "This is where the power plant admin staff and operators are housed.\n\nIt "
                           "has both the Power Station LAN and Enterprise WAN.",
            "name": "Administration Block",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F3",
            "impact": {
                "confidentiality": "5",
                "id": "POWER-STATION-BIL5",
                "integrity": "4",
                "availability": "5"
            },
            "sensitivity": 1
        }, {
            "id": "POWER-STATION-A6",
            "assetType": "physical",
            "description": "This is the military controlled accommodation.",
            "name": "Military Compound",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F4",
            "impact": {
                "confidentiality": "5",
                "id": "POWER-STATION-BIL6",
                "integrity": "4",
                "availability": "3"
            },
            "sensitivity": 4
        }, {
            "id": "POWER-STATION-C1",
            "assetType": "cyber",
            "description": "The reactor generates thermal heat by causing a nuclear reaction. \n\nThe "
                           "course control system is powered by the station 50V DC battery.",
            "name": "Reactor HMI and ICS",
            "group": "POWER-STATION-G1",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL7",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-C2",
            "assetType": "cyber",
            "description": "The turbines are responsible for generating electricity from the stream "
                           "generated by the thermal heat.",
            "name": "Gas Turbines HMI and ICS",
            "group": "POWER-STATION-G1",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL8",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 5
        }, {
            "id": "POWER-STATION-C3",
            "assetType": "cyber",
            "description": "The pumping station is required to deliver the water that is used to extract "
                           "the heat from the gas and convert it into steam for the generators.",
            "name": "Pump Water coolant House HMI and ICS",
            "group": "POWER-STATION-G1",
            "function": "POWER-STATION-F1",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL9",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 4
        }, {
            "id": "POWER-STATION-C4",
            "assetType": "cyber",
            "description": "The power distribution system stores and switches the power generated to "
                           "deliver to the national grid.",
            "name": "Switch Compound HMI and ICS",
            "group": "POWER-STATION-G1",
            "function": "POWER-STATION-F2",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL10",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-C5",
            "assetType": "cyber",
            "description": "Manages the nuclear waste material that is generated as a result of the "
                           "Nuclear Reactors.",
            "name": "Waste Treatment HMI and ICS",
            "group": "POWER-STATION-G1",
            "function": "POWER-STATION-F3",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL11",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-C6",
            "assetType": "cyber",
            "description": "The enterprise network used to locally manage the ICT requirements of the "
                           "Power plant.",
            "name": "Power Station LAN",
            "group": "POWER-STATION-G2",
            "function": "POWER-STATION-F3",
            "impact": {
                "confidentiality": "4",
                "id": "POWER-STATION-BIL12",
                "integrity": "3",
                "availability": "3"
            },
            "sensitivity": 4
        }, {
            "id": "POWER-STATION-C7",
            "assetType": "cyber",
            "description": "The enterprise network used to manage the wider ICT requirements of the "
                           "Power plant including interconnections with other Power Stations and other "
                           "organisation units belonging to the same organisation.",
            "name": "Power Station Enterprise WAN",
            "group": "POWER-STATION-G2",
            "function": "POWER-STATION-F2",
            "impact": {
                "confidentiality": "4",
                "id": "POWER-STATION-BIL13",
                "integrity": "3",
                "availability": "3"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-C8",
            "assetType": "cyber",
            "description": "The connections with the Internet and any or all other organisations that "
                           "require and ICT connection with the Trawsfynydd Power station and parent company.",
            "name": "Internet Access",
            "group": "POWER-STATION-G2",
            "function": "POWER-STATION-F3",
            "impact": {
                "confidentiality": "3",
                "id": "POWER-STATION-BIL14",
                "integrity": "2",
                "availability": "2"
            },
            "sensitivity": 3
        }, {
            "id": "POWER-STATION-C9",
            "assetType": "cyber",
            "description": "The military network that connects to other parts of the UK military network "
                           "in order to meet the tasking order.",
            "name": "Military Network",
            "group": "POWER-STATION-G3",
            "function": "POWER-STATION-F4",
            "impact": {
                "confidentiality": "5",
                "id": "POWER-STATION-BIL15",
                "integrity": "5",
                "availability": "5"
            },
            "sensitivity": 4
        }],
        "threats": [
            {
                "assetsThreatened": ["POWER-STATION-A1"],
                "name": "Insider",
                "motivation": "Disgruntled, lured by financial gains, Leaving the organisation, post "
                              "disciplinary situation, Bribed/ Blackmailed, Coerced or Tricked",
                "id": "POWER-STATION-TA1",
                "threatLevel": "SEVERE",
                "purpose": "This would allow them to affect the stability and safety of the power plant "
                           "for financial, political, personal or religious gain.",
                "intent": "They would want to Collect/Gather, reveal or divulge, or even corrupt/change "
                          "or destroy the information that the power plant systems use."
            }, {
                "assetsThreatened": ["POWER-STATION-A3", "POWER-STATION-C8"],
                "name": "Hacker",
                "motivation": "Curious, Intellectual challenge, Patriotic, Political, financial, organised "
                              "crime or state sponsored.",
                "id": "POWER-STATION-TA2",
                "threatLevel": "MODERATE",
                "purpose": "This would allow them to affect the stability and safety of the power plant for "
                           "financial, political or personal gain.",
                "intent": "They would want to Collect/Gather, reveal or divulge, or even corrupt/change or "
                          "destroy the information that the power plant systems use."
            }],
        "vulnerabilities": [{
            "assets": ["POWER-STATION-A3", "POWER-STATION-C8"],
            "description": "No standard patching regime in place.",
            "name": "No patching regime",
            "type": "cyber",
            "id": "POWER-STATION-V1"
        }, {
            "assets": ["POWER-STATION-A1"],
            "description": "Entrance into main reactor building is unsecured",
            "name": "Unsecured entrance",
            "type": "physical",
            "id": "POWER-STATION-V2"
        }, {
            "assets": ["POWER-STATION-A1"],
            "description": "Known cyber vulnerability for reactor core software",
            "name": "Software vulnerability",
            "type": "cyber",
            "id": "POWER-STATION-V3"
        }],
        "networks": [{
            "id": "ENT-NETWORK",
            "name": "Enterprise network",
            "description": "An enterprise network of cyber devices"
        }]
    }
]
