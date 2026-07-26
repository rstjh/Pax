from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from drf_yasg.utils import swagger_auto_schema

from api.services.courses_of_action_store import (
    add_task,
    create_course_of_action,
    delete_course_of_action,
    delete_task,
    get_courses_of_action
)


class CourseOfActionListView(ListCreateAPIView):
    """
    Courses of action stored for a mission.
    """
    renderer_classes = (JSONRenderer,)

    @swagger_auto_schema(responses={200: "OK"})
    def get(self, request, *args, **kwargs):
        return Response(
            data=get_courses_of_action(self.kwargs['missionId']),
            status=200)

    # Implement the get_queryset to stop warnings of schema generation
    def get_queryset(self):
        return None


class CourseOfActionView(ListCreateAPIView, RetrieveDestroyAPIView):
    """
    Create or delete a single course of action. Mirrors the external C2's
    `coa/mission/{missionId}/coa/{coa}` route, where the trailing segment is
    the new course of action's name on POST and its id on DELETE.
    """
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        return Response(
            data=create_course_of_action(
                mission_id=self.kwargs['missionId'],
                name=self.kwargs['coa']),
            status=201)

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, *args, **kwargs):
        deleted = delete_course_of_action(
            mission_id=self.kwargs['missionId'],
            coa_id=self.kwargs['coa'])
        if not deleted:
            return Response(
                data={'detail': 'No such course of action.'},
                status=404)
        return Response(status=204)


class CourseOfActionTaskView(ListCreateAPIView):
    """
    Tasks staged against a course of action.
    """
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={201: "Created"})
    def post(self, request, *args, **kwargs):
        task = add_task(
            mission_id=self.kwargs['missionId'],
            coa_id=self.kwargs['coa'],
            task=request.data)
        if task is None:
            return Response(
                data={'detail': 'No such course of action.'},
                status=404)
        return Response(
            data=task,
            status=201)


class CourseOfActionTaskDetailView(RetrieveDestroyAPIView):
    renderer_classes = (JSONRenderer,)

    def get_queryset(self):
        return None

    @swagger_auto_schema(responses={204: "No content"})
    def delete(self, request, *args, **kwargs):
        deleted = delete_task(
            mission_id=self.kwargs['missionId'],
            coa_id=self.kwargs['coa'],
            task_id=self.kwargs['taskId'])
        if not deleted:
            return Response(
                data={'detail': 'No such course of action.'},
                status=404)
        return Response(status=204)
