from django.db import models
from user import User
from lecture import Lecture

class Lecturer(User):
    profession = models.CharField(max_length=100)
    lectures = models.ForeignKey(Lecture)
    
    class Meta:
        app_label = "Learn"