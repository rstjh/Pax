from Pax import api_config
from django.conf.urls import url
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework.urlpatterns import format_suffix_patterns

from api.views.action_estimated_time import ActionEstimatedTime
from api.views.action_instances import ActionInstancesView
from api.views.coa import CourseOfActionListView, CourseOfActionView, \
    CourseOfActionTaskView, CourseOfActionTaskDetailView
from api.views.action_list import ActionListForceDetail, ActionListForceEffectDetail
from api.views.action_templates import ActionTemplatesView
from api.views.courses_of_action import GenerateCoursesOfAction
from api.views.cvi_systems import CVIView, CVISystemView
from api.views.effects import EffectsView
from api.views.geolocation import AssetActorDistance
from api.views.hostile_responses import HostileResponsesView, HostileResponseDetailView
from api.views.index import IndexView
from api.views.missions import MissionIdView, MissionsView
from api.views.system import SystemMissionTime
from api.views.units import UnitsView
from api.views.reset import ResetData
from api.views.risk_appetite import RiskAppetiteDetail, RiskAppetiteView
from api.views.risk import NetworkRiskAnalysis, SystemRiskAnalysis, \
    CompareSystemRiskAnalysis, TaskDependencyRiskAnalysis


SchemaView = get_schema_view(
    openapi.Info(
        title="Pax API",
        default_version=api_config.API_VERSION,
        description="Pax API documentation",
    ),
    validators=['ssv', 'flex'],
    public=True
)

urlpatterns = format_suffix_patterns([
    # Risk analysis
    url(r'^api/v{}/risk_analysis/network/(?P<systemId>.+)/$'.format(
        api_config.API_VERSION),
        NetworkRiskAnalysis.as_view()),

    url(r'^api/v{}/risk_analysis/system/(?P<systemId>.+)/$'.format(
        api_config.API_VERSION),
        SystemRiskAnalysis.as_view()),

    url(r'^api/v{}/risk_analysis/task_dependency/(?P<systemId>.+)/$'.format(
        api_config.API_VERSION),
        TaskDependencyRiskAnalysis.as_view()),

    url(r'^api/v{}/risk_analysis/compare_system/(?P<systemId>.+)/$'.format(
        api_config.API_VERSION),
        CompareSystemRiskAnalysis.as_view()),

    # Effects
    url(r'^api/v{}/effects/$'.format(
        api_config.API_VERSION),
        EffectsView.as_view()),

    # Hostile responses
    url(r'^api/v{}/hostile_response/$'.format(
        api_config.API_VERSION),
        HostileResponsesView.as_view()),

    url(r'^api/v{}/hostile_response/(?P<effect>[^/]+)/$'.format(
        api_config.API_VERSION),
        HostileResponseDetailView.as_view()),

    # Risk appetite
    url(r'^api/v{}/risk_appetite/$'.format(
        api_config.API_VERSION),
        RiskAppetiteView.as_view()),

    url(r'^api/v{}/risk_appetite/(?P<missionId>.+)/$'.format(
        api_config.API_VERSION),
        RiskAppetiteDetail.as_view()),

    # Action templates
    url(r'^api/v{}/action_templates/$'.format(
        api_config.API_VERSION),
        ActionTemplatesView.as_view()),

    # Action instances
    url(r'^api/v{}/action_instances/$'.format(
        api_config.API_VERSION),
        ActionInstancesView.as_view()),

    # Geolocation
    url(r'^api/v{}/geolocation/distance/(?P<systemId>[^/]+)/(?P<assetId>[^/]+)/(?P<actorId>[^/]+)/$'.format(
        api_config.API_VERSION),
        AssetActorDistance.as_view()),

    # Estimated task times
    url(r'^api/v{}/actions/estimated_time/(?P<systemId>.+)/$'.format(
        api_config.API_VERSION),
        ActionEstimatedTime.as_view()),

    # Action list
    url(r'^api/v{}/action_list/all/(?P<force>.+)/$'.format(
        api_config.API_VERSION),
        ActionListForceDetail.as_view()),

    url(r'^api/v{}/action_list/type/(?P<force>.+)/(?P<effect>.+)/(?P<type>.+)/$'.format(
        api_config.API_VERSION),
        ActionListForceEffectDetail.as_view()),

    # Courses of action (local stand-in for the C2's coa/... routes)
    url(r'^api/v{}/coa/mission/(?P<missionId>[^/]+)/coa/$'.format(
        api_config.API_VERSION),
        CourseOfActionListView.as_view()),

    url(r'^api/v{}/coa/mission/(?P<missionId>[^/]+)/coa/(?P<coa>[^/]+)/task$'.format(
        api_config.API_VERSION),
        CourseOfActionTaskView.as_view()),

    url(r'^api/v{}/coa/mission/(?P<missionId>[^/]+)/coa/(?P<coa>[^/]+)/task/(?P<taskId>[^/]+)$'.format(
        api_config.API_VERSION),
        CourseOfActionTaskDetailView.as_view()),

    url(r'^api/v{}/coa/mission/(?P<missionId>[^/]+)/coa/(?P<coa>[^/]+)$'.format(
        api_config.API_VERSION),
        CourseOfActionView.as_view()),

    # Course of action
    url(r'api/v{}/course_of_action/generate/$'.format(
        api_config.API_VERSION),
        GenerateCoursesOfAction.as_view()),

    # System
    url(r'^api/v{}/system/mission_time/(?P<systemId>.+)/'.format(
        api_config.API_VERSION),
        SystemMissionTime.as_view()),

    # CVI
    url(r'^api/v{}/cvi/'.format(
        api_config.API_VERSION),
        CVIView.as_view()),

    url(r'^api/v{}/cvi/(?P<systemId>.+)/'.format(
        api_config.API_VERSION),
        CVISystemView.as_view()),

    # Units
    url(r'^api/v{}/units/$'.format(
        api_config.API_VERSION),
        UnitsView.as_view()),

    # Mission
    url(r'^api/v{}/missions/'.format(
        api_config.API_VERSION),
        MissionsView.as_view()),

    url(r'^api/v{}/missions/(?P<missionId>.+)/'.format(
        api_config.API_VERSION),
        MissionIdView.as_view()),

    # Reset
    url(r'^api/v{}/reset/'.format(
        api_config.API_VERSION),
        ResetData.as_view()),

    # Swagger
    url(r'^swagger/$',
        SchemaView.with_ui('swagger', cache_timeout=0),
        name='schema-swagger-ui'),

    url(r'^redoc/$',
        SchemaView.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),

    # Angular
    url(r'^$',
        IndexView.as_view(),
        name='index'),

    url(r'^(?P<path>.*)/$',
        IndexView.as_view()),
])
