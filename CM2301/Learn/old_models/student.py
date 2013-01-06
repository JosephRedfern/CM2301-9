from django.db import models
from user import User

class Student(User):
    student_number = models.CharField(max_length=50)
    course_enrolled = models.CharField(max_length=50)
    
    class Meta:
        app_label = "Learn"