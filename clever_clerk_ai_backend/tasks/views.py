from datetime import datetime
from django.utils.timezone import now
from rest_framework.decorators import action
from rest_framework import viewsets, mixins, status

from .helpers.response import api_response
from .models import Task, ContextEntry
from .serializers import TaskSerializer, ContextEntrySerializer


class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user).order_by('-createdAt')

    def create(self, request, *args, **kwargs):
        many = isinstance(request.data, list)
        serializer = self.get_serializer(data=request.data, many=many)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return api_response(
            success=True,
            data=serializer.data,
            successText="Task(s) created",
            status_code=status.HTTP_201_CREATED
        )
    
    def update(self, request, *args, **kwargs):
        partial = kwargs.pop("partial", False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial
        )
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return api_response(
            success=True,
            data=serializer.data,
            successText="Task updated",
            status_code=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance.delete()
        return api_response(
            data=None,
            success=True,
            successText="Task deleted",
            status_code=status.HTTP_204_NO_CONTENT
        )
    
    @action(detail=False, methods=["get"])
    def today(self, request):
        """GET /api/tasks/today/"""
        today_start = now().replace(hour=0, minute=0, second=0, microsecond=0)
        tasks = self.get_queryset().filter(deadline__gte=today_start, deadline__lt=today_start.replace(hour=23,minute=59))
        data = TaskSerializer(tasks, many=True).data
        return api_response(
            data=data,
            success=True, 
            successText="Today's tasks", 
            status_code=status.HTTP_200_OK
        )

class ContextEntryViewSet(mixins.ListModelMixin, mixins.UpdateModelMixin, mixins.DestroyModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    serializer_class = ContextEntrySerializer

    def get_queryset(self):
        return ContextEntry.objects.filter(task__user=self.request.user)
    
    def create(self, request, *args, **kwargs):
        ser = self.get_serializer(data=request.data)
        ser.is_valid(raise_exception=True)
        ct = ser.save()
        return api_response(
            success=True,
            successText="Context entry added",
            data=ContextEntrySerializer(ct).data,
            status_code=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        ser = self.get_serializer(
            self.get_object(), data=request.data, partial=kwargs.pop("partial", False)
        )
        ser.is_valid(raise_exception=True)
        ct = ser.save()
        return api_response(
            success=True, 
            data=ser.data,
            successText="Context updated", 
            status_code=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        self.get_object().delete()
        return api_response(
            data=None,
            success=True,
            successText="Context entry deleted",
            status_code=status.HTTP_204_NO_CONTENT
        )
