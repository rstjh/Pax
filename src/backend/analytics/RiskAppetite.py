import os

import numpy as np
import pymongo as pm


_author_ = 'Owen Sims (sims.owen@gmail.com)'


def get_risk_appetite(system_id):
    client = pm.MongoClient(host=os.environ.get('DB_HOSTNAME'), port=int(os.environ.get('DB_PORT')))
    ra_collection = client[os.environ.get('DB_NAME')]['risk_appetite']
    risk_appetite_data = ra_collection.find_one({"systemId": system_id})
    return risk_appetite_data


class RiskAppetiteAnalysis:
    """
    A class that generates a risk appetite score from data inserted in the
    Mongo collection `risk-appetite-data`.
    """
    def __init__(self, risk_appetite_data):
        """
        Initialise the class by collecting the risk appetite data and stores it
        as a dictionary.
        """
        self.riskAppetiteData = risk_appetite_data

    def generate_asset_weights(self):
        # How does the organization prioritize cyber assets over physical assets?
        physicalAssetQuantities = []
        physicalQuestions = [
        'riskAssetImportance',
        'riskQuantity',
        'currentSecurityRegimeImportance',
        'impactReplacingAssets',
        'impactDefenceEffort'
        ]

        # Find the relative weights attached to physical assets relative to cyber assets
        for i in range(len(physicalQuestions)):
            totalPhysical = float(self.riskAppetiteData[physicalQuestions[i]]['physicalAssets']) + float(self.riskAppetiteData[physicalQuestions[i]]['cyberAssets'])
            physicalAssetQuantities.append(float(self.riskAppetiteData[physicalQuestions[i]]['physicalAssets']) / totalPhysical)

        # Take some average of these weights
        physicalAssetWeight = np.mean(physicalAssetQuantities)

        # Return weights for physical and cyber assets
        return [physicalAssetWeight, 1 - physicalAssetWeight]

    # Questions scored into the risk appetite. Each is a matrix question with
    # a physicalAssets and a cyberAssets row. Not every questionnaire asks all
    # of them, so the score averages whichever are answered.
    SCORED_QUESTIONS = (
        'riskAssetImportance',
        'currentSecurityRegimeImportance',
        'impactDefenceEffort'
    )

    def _question_score(self, question):
        answer = self.riskAppetiteData.get(question)
        if not answer:
            return None
        if 'cyberAssets' not in answer or 'physicalAssets' not in answer:
            return None
        return (float(answer['cyberAssets']) +
                float(answer['physicalAssets'])) / 10

    def generate_risk_appetite_score(self):
        riskAppetiteItems = [
            score for score in (
                self._question_score(question)
                for question in self.SCORED_QUESTIONS
            ) if score is not None
        ]

        if not riskAppetiteItems:
            raise ValueError(
                "Risk appetite data answered none of: {}".format(
                    ', '.join(self.SCORED_QUESTIONS)))

        riskAppetiteScore = np.mean(riskAppetiteItems) * 100

        return int(riskAppetiteScore)

    def generate_risk_appetite_label(self, riskAppetiteScore):
        """
        Bucket the risk appetite score to generate a relevant label
        """
        # Bucketing operation
        if riskAppetiteScore >= 87:
            riskAppetiteLabel = "Very risk loving"
        elif riskAppetiteScore >= 75:
            riskAppetiteLabel = "Risk loving"
        elif riskAppetiteScore >= 50:
            riskAppetiteLabel = "Risk neutral"
        elif riskAppetiteScore >= 25:
            riskAppetiteLabel = "Risk averse"
        else:
            riskAppetiteLabel = "Very risk averse"

        return riskAppetiteLabel
