from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet,DoctorViewSet,PatientViewSet,
    DoctorRegistrationView,PatientRegistrationView
)

router = DefaultRouter()
router.register(r'users',UserViewSet)
router.register(r'doctors', DoctorViewSet)
router.register(r'patients', PatientViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('register/doctor/', DoctorRegistrationView.as_view(), name='doctor-registration'),
    path('register/patient/', PatientRegistrationView.as_view(), name='patient-registration'),
]
