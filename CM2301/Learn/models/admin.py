from django.db import models
from user import User

class Admin(User):
    profession = models.CharField(max_length=50)
    
    class Meta:
        app_label = "Learn"