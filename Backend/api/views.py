import io
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt

from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import HttpResponse

# ReportLab for professional PDF building
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader

from .models import UploadedDataset
from .serializers import UserSerializer, DatasetSerializer

# AUTHENTICATION 
class RegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

#  CORE DATA PROCESSING 
class EquipmentUploadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        file = request.FILES.get('file')
        if not file:
            return Response({"error": "No file provided"}, status=400)

        try:
            df = pd.read_csv(file)
            
            # Perform calculations and round to 2 decimals 
            summary = {
                'total_count': len(df),
                'avg_temp': round(float(df['Temperature'].mean()), 2),
                'avg_pressure': round(float(df['Pressure'].mean()), 2),
                'avg_flow': round(float(df['Flowrate'].mean()), 2),
                'type_dist': df['Type'].value_counts().to_dict()
            }

            # Save dataset record to the Database
            record = UploadedDataset.objects.create(
                user=request.user,
                filename=file.name,
                total_count=summary['total_count'],
                avg_temp=summary['avg_temp'],
                avg_pressure=summary['avg_pressure'],
                avg_flow=summary['avg_flow'],
                type_dist=summary['type_dist']
            )

            return Response({
                "id": record.id,
                "summary": summary,
                "raw_data": df.to_dict(orient='records')
            })
        except Exception as e:
            return Response({"error": str(e)}, status=500)

# HISTORY RETRIEVAL 
class HistoryView(generics.ListAPIView):
    serializer_class = DatasetSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Fetch only the current user's last 5 uploads
        return UploadedDataset.objects.filter(user=self.request.user).order_by('-uploaded_at')[:5]

#PROFESSIONAL PDF GENERATION
class GeneratePDF(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, record_id):
        try:
            record = UploadedDataset.objects.get(id=record_id)
        except UploadedDataset.DoesNotExist:
            return HttpResponse("Report Not Found", status=404)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = f'attachment; filename="Equipment_Report_{record.id}.pdf"'

        p = canvas.Canvas(response, pagesize=letter)
        width, height = letter

        # 1. Page Header
        p.setFont("Helvetica-Bold", 18)
        p.setStrokeColorRGB(0.12, 0.23, 0.47)
        p.drawString(50, height - 50, "CHEMICAL EQUIPMENT ANALYSIS REPORT")
        p.line(50, height - 60, width - 50, height - 60)
        
        p.setFont("Helvetica", 10)
        p.drawString(50, height - 75, f"Source File: {record.filename}")
        p.drawString(width - 220, height - 75, f"Processed: {record.uploaded_at.strftime('%Y-%m-%d %H:%M')}")

        # 2. Key Statistics
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 110, "Summary Analytics:")
        p.setFont("Helvetica", 11)
        p.drawString(70, height - 130, f"• Total Equipment Count: {record.total_count} units")
        p.drawString(70, height - 145, f"• Mean Operating Temperature: {record.avg_temp} C")
        p.drawString(70, height - 160, f"• Mean Operating Pressure: {record.avg_pressure} bar")
        p.drawString(70, height - 175, f"• Mean System Flowrate: {record.avg_flow} m3/h")

        # 3. Embed Pie Chart 
        p.setFont("Helvetica-Bold", 12)
        p.drawString(50, height - 210, "Equipment Distribution")
        
        plt.figure(figsize=(4, 3))
        plt.pie(record.type_dist.values(), labels=record.type_dist.keys(), autopct='%1.1f%%', colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'])
        
        pie_buf = io.BytesIO()
        plt.savefig(pie_buf, format='png', bbox_inches='tight', transparent=True)
        plt.close() # Freeing the  memory
        pie_buf.seek(0)
        p.drawImage(ImageReader(pie_buf), 40, height - 420, width=240, height=180)

        # 4. Embed Bar Chart 
        p.drawString(320, height - 210, "Parameter Overview")
        
        plt.figure(figsize=(4, 3))
        plt.bar(['Pressure', 'Temp', 'Flow'], [record.avg_pressure, record.avg_temp, record.avg_flow], color='#3b82f6')
        
        bar_buf = io.BytesIO()
        plt.savefig(bar_buf, format='png', bbox_inches='tight', transparent=True)
        plt.close() # Freeing memory
        bar_buf.seek(0)
        p.drawImage(ImageReader(bar_buf), 310, height - 420, width=240, height=180)

        # 5. Footer
        p.setFont("Helvetica-Oblique", 8)
        p.line(50, 40, width - 50, 40)
        p.drawString(50, 30, "System Generated Analytics | Private and Confidential")

        p.showPage()
        p.save()
        return response