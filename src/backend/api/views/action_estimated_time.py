from drf_yasg.utils import swagger_auto_schema

from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer

from analytics.ActionAnalysis import get_action_time
from analytics.SystemAnalysis import asset_from_id

from api.views.c2_data_requestor import C2DataRequestor


# The action_list collection holds a single time per (effect, asset type), not
# a distribution, so the spread shown on the candlestick chart is a fixed
# uncertainty band around that point estimate.
INTER_QUARTILE_SPREAD = 0.25
WHISKER_SPREAD = 0.5


def estimate_task_time(task, assets):
    """
    Estimate how long a task will take, with a spread for the chart's
    candlesticks: [minimum, lower quartile, upper quartile, maximum].
    """
    objective_type = asset_from_id(
        asset_id=task['objective'],
        assets=assets,
        asset_type=True)

    estimated_time = None
    if objective_type is not None:
        try:
            estimated_time = get_action_time(
                effect=task['effect'],
                type=objective_type)
        except (TypeError, KeyError):
            estimated_time = None

    if estimated_time is None:
        # Nothing recorded for this effect and asset type: fall back to the
        # time frame the planner allowed for the task.
        estimated_time = task.get('timeFrame') or 0

    estimated_time = float(estimated_time)
    return {
        'estimatedTime': estimated_time,
        'quartiles': [
            estimated_time * (1 - WHISKER_SPREAD),
            estimated_time * (1 - INTER_QUARTILE_SPREAD),
            estimated_time * (1 + INTER_QUARTILE_SPREAD),
            estimated_time * (1 + WHISKER_SPREAD)
        ]
    }


class ActionEstimatedTime(C2DataRequestor):
    """
    Estimate the time each task in a course of action will take, keyed by
    task id, for the course of action review chart.
    """
    renderer_classes = (JSONRenderer,)

    @swagger_auto_schema(responses={200: "OK"})
    def post(self, request, *args, **kwargs):
        return self.fetch_c2_data(request.data, self.kwargs['systemId'])

    def status_200(self, system_id, action_data, system_data):
        assets = system_data['assets']
        return Response(
            data={
                task['taskId']: estimate_task_time(task, assets)
                for task in action_data
            },
            status=200)
