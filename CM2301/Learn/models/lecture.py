from django.db import models

class Lecture(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    title = models.CharField(max_length=100)
    module = models.CharField(max_length=50)
    videos = models.CharField(max_length=50)
    attachments = models.CharField(max_length=50)
    visible = models.BooleanField()
    links = models.CharField(max_length=50)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())
    
    class Meta:
        app_label = "Learn"
        
    