from django.db import models

class Queue(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    title = models.CharField(max_length=100)
    
    class Meta:
        app_label = "Learn"