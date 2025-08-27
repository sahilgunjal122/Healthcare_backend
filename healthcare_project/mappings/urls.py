
from django.urls import path
from .views import (
    PatientDoctorMappingListCreateView,
    PatientSpecificDoctorsListView,
    PatientDoctorMappingDeleteView
)

urlpatterns = [
    path('', PatientDoctorMappingListCreateView.as_view(), name='mapping-list-create'),
    path('<int:patient_pk>/', PatientSpecificDoctorsListView.as_view(), name='patient-doctors-list'),
    path('<int:patient_pk>/<int:doctor_pk>/', PatientDoctorMappingDeleteView.as_view(), name='mapping-delete'),
]