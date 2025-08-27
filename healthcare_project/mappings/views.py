
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import PatientDoctorMapping, Patient, Doctor
from .serializers import PatientDoctorMappingSerializer
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import ValidationError

class PatientDoctorMappingListCreateView(generics.ListCreateAPIView):
    queryset = PatientDoctorMapping.objects.all()
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return PatientDoctorMapping.objects.filter(patient__creator=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        patient = serializer.validated_data.get('patient')
        if patient.creator != self.request.user:
            return Response(
                {"detail": "You do not have permission to assign a doctor to this patient."},
                status=status.HTTP_403_FORBIDDEN
            )
        
        doctor = serializer.validated_data.get('doctor')
        if doctor.creator != self.request.user:
            return Response(
                {"detail": "You do not have permission to use this doctor for mapping."},
                status=status.HTTP_403_FORBIDDEN
            )

        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class PatientSpecificDoctorsListView(generics.ListAPIView):
    serializer_class = PatientDoctorMappingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        patient_pk = self.kwargs.get('patient_pk')
        patient = get_object_or_404(Patient, pk=patient_pk)

        if patient.creator != self.request.user:
            return PatientDoctorMapping.objects.none()

        return PatientDoctorMapping.objects.filter(patient=patient)

class PatientDoctorMappingDeleteView(generics.DestroyAPIView):
    queryset = PatientDoctorMapping.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        patient_pk = self.kwargs.get('patient_pk')
        doctor_pk = self.kwargs.get('doctor_pk')

        patient = get_object_or_404(Patient, pk=patient_pk, creator=self.request.user)
        doctor = get_object_or_404(Doctor, pk=doctor_pk, creator=self.request.user)

        try:
            return PatientDoctorMapping.objects.get(patient=patient, doctor=doctor)
        except PatientDoctorMapping.DoesNotExist:
            raise ValidationError("Mapping does not exist.")
