import os

import pymongo as pm
from django.http import HttpResponse
from rest_framework.views import APIView

from analytics.Fair import capability_rollup
from utils.ReportGenerator import generate_summary_report


def _db():
    return pm.MongoClient(
        host=os.environ.get('DB_HOSTNAME'),
        port=int(os.environ.get('DB_PORT'))
    )[os.environ.get('DB_NAME')]


class ReportSummaryDocxView(APIView):
    """GET /reports/summary.docx — downloadable Word summary report (F8)."""

    def __init__(self):
        database = _db()
        self.risks_collection = database['risks']
        self.controls_collection = database['controls']
        self.techniques_collection = database['attackTechniques']
        self.roadmap_collection = database['roadmapPlan']

    def get(self, request, *args, **kwargs):
        risks = list(self.risks_collection.find({}))
        controls = list(self.controls_collection.find({}))
        techniques = list(self.techniques_collection.find({}, {'_id': 0}))
        plan_entries = list(self.roadmap_collection.find({}))

        risk_counts = {'open': 0, 'in_progress': 0, 'closed': 0}
        for risk in risks:
            risk_counts[risk.get('status', 'open')] = risk_counts.get(risk.get('status', 'open'), 0) + 1

        top_gaps = []
        for technique in techniques:
            mapped_count = len([
                control for control in controls
                if technique['id'] in control.get('attackTechniqueIds', [])
            ])
            if mapped_count == 0:
                top_gaps.append({
                    'techniqueId': technique['id'],
                    'techniqueName': technique['name'],
                    'controlCount': 0,
                })

        controls_by_id = {str(control['_id']): control for control in controls}
        roadmap = []
        for entry in plan_entries:
            control = controls_by_id.get(entry.get('controlId'), {})
            roadmap.append({
                'controlName': control.get('name', entry.get('controlId', 'Unknown control')),
                'quarter': entry.get('quarter', ''),
                'status': entry.get('status', ''),
                'rationale': entry.get('rationale', ''),
            })

        summary = {
            'totalResidualAle': capability_rollup(risks),
            'riskCounts': risk_counts,
            'topGaps': top_gaps[:10],
            'roadmap': roadmap,
        }
        document_buffer = generate_summary_report(summary)

        response = HttpResponse(
            document_buffer.read(),
            content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = 'attachment; filename="risk-roadmap-summary.docx"'
        return response
