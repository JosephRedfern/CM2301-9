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
    """
    A UserField is a value attached to a user.
    Users can have multiple UserFields
    """
    user = models.ForeignKey(User)
    key = models.CharField(max_length=250)
    value = models.CharField(max_length=250)

class Attachment(Base):
    """
    An attachment is a collection of revisions. 
    
    Attachment objects can be used to derive a full file revision history, 
    and retrieve the original version of the file
    """
    title = models.CharField(max_length=50)
    file_type = models.CharField(max_length=50)
    description = models.CharField(max_length=250)
    revision = models.CharField(max_length=50)
    owner = models.ForeignKey(User)
    
    def get_total_size(self):
        """
        Returns the total size used of all revisions
        """
        return
    
    def remove_revision(self, revision_uuid):
        """
        Removes the revision from the attachment with the 
        specified uuid.
        
            Args:
                revision_uuid - The UUID of the revision you wish to purge
            Returns:
                None
        """
        return

class Lecture(Base):
    """
    Represents a lecture within a module.
    Contains details about an individual lecture & references to
    lecture content (Videos, Attachments and Lecture Notes).
    """
    title = models.CharField(max_length=50)
    modules = models.ManyToManyField(Module)
    videos = models.ManyToManyField(Video)
    attachments = models.ManyToManyField(Attachment)
    validFrom = models.DateField()
    validTo = models.DateField()
    visible = models.BooleanField(default=True)
    links = models.ManyToManyField(Link)
    lectureMaterials = models.ManyToManyField(LectureMaterial)
