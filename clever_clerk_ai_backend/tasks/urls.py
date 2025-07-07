from rest_framework.routers import DefaultRouter
from .views import TaskViewSet, ContextEntryViewSet

router = DefaultRouter()
router.register(r"tasks", TaskViewSet, basename="tasks")
router.register(r"context", ContextEntryViewSet, basename="context")

urlpatterns = router.urls