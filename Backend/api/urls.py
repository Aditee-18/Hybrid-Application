from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import RegisterView, EquipmentUploadView, HistoryView, GeneratePDF

urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('upload/', EquipmentUploadView.as_view(), name='file_upload'),
    path('history/', HistoryView.as_view(), name='history'),
    path('pdf/<int:record_id>/', GeneratePDF.as_view(), name='generate_pdf'),
]