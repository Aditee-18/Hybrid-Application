from django.db import models
from django.contrib.auth.models import User

class UploadedDataset(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    filename = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    # Store summaries so we don't have to re-calculate every time
    total_count = models.IntegerField()
    avg_temp = models.FloatField()
    avg_pressure = models.FloatField()
    avg_flow = models.FloatField()
    
    # store the distribution as a JSON string
    type_dist = models.JSONField(default=dict) 

    def __str__(self):
        return f"{self.filename} - {self.uploaded_at}"