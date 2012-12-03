from django.db import models
import uuid

# Create your models here.

class QueueItem(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    job_type = models.CharField(max_length=50)
    submission_time = models.DateTimeField(auto_now_add = True)
    waiting = models.BooleanField()
    progress = models.FloatField(null=True)
    completion_time = models.DateTimeField(null=True)
    
    def __init__(self, *args, **kwargs):
        super(QueueItem, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())

class Server(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    server_alias = models.CharField(max_length=200)
    hostname = models.CharField(max_length=200)
    os = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    load = models.FloatField(null=True)
    
    def __init__(self, *args, **kwargs):
        super(Server, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())
        
class User(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50)
    
    def __init__(self, *args, **kwargs):
        super(User, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())
        
class Student(User):
    student_number = models.CharField(max_length=50)
    course_enrolled = models.CharField(max_length=50)
    
class Lecturer(User):
    profession = models.CharField(max_length=50)
    
class UserPreference(models.Model):
    uuid = models.CharField(max_length=36, primary_key=True)
    user = models.ForeignKey(User)
    key =  models.CharField(max_length=50)
    content =  models.CharField(max_length=150)