from django.db import models

class User(models.Model):
    
    class Meta:
        app_label = 'learn'
    
    uuid = models.CharField(max_length=36, primary_key=True)
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())