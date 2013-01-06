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
    
    def delete_all_revisions(self):
        """
        Revisions all revisions but the most recent from the attachment object
        """
        return
    
    def get_all_revisions(self):
        """
        Returns an ordered List of revisions for the Attachment based on time uploaded.
        """
        
class Revision(Base):
    """
    A revision object represents a single file that belongs to an attachment, 
    this class allows attachments to have full versioning.
    """
    TimeUploaded = models.DateTimeField(auto_now_add=True)
    File = models.FileField()
    Approved = models.BooleanField()
    UploadedBy = models.ForeignKey(User)
    FileSize = models.FloatField()
    
    def get_file(self):
        """Returns the File object for the current revision"""
        return
    
class Link(Base):
    """Holds a link for other objects, both external and internal"""
    title = models.CharField(max_length=250)
    description = models.TextField()
    link = models.URLField(max_length=250)

class Video(Base):
    """
    Represents a video.
    Contains video title, keywords and description.
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

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


