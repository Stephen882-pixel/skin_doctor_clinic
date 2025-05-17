from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AppointmentViewSet, DoctorScheduleViewSet, DoctorTimeOffViewSet
)

router = DefaultRouter()
router.register(r'appointments', AppointmentViewSet)
router.register(r'schedules', DoctorScheduleViewSet)
router.register(r'time-offs', DoctorTimeOffViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
