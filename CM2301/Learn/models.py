from django.db import models
import uuid

class Base(models.Model):
    
    uuid = models.CharField(max_length=36, primary_key=True)
    
    def __init__(self, *args, **kwargs):
        super(Base, self).__init__(*args, **kwargs)
        self.uuid = str(uuid.uuid4())
    
    class Meta:
        abstract = True
        
class User(Base):
    """
    Represents any user of the system. 
    A User contains attributes that are common for any user of the system.
    """
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    email = models.CharField(max_length=75)
    phone = models.EmailField(max_length=20)
    
class UserField(Base):
    user = models.ForeignKey(User)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

class Attachment(Base):
    title = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    revision = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    
    def get_total_size(self):
        return
    
    def remove_revision(self):
        return
    