from django.db import models
import uuid

class Base(models.Model):
    """
    Base class containing common properties and methods for models.
    
    All models will extend this class.
    """
    
    """UUID of the object, as String"""
    uuid = models.CharField(max_length=36, primary_key=True)
    
    def save(self, *args, **kwargs):
        """
        Overrides the django.model.save() method to add a random UUID
        to new objects before they are persisted to the DB.
        """
        if not self.uuid:
            uuid = str(uuid.uuid4())
        super(Base, self).save(*args, **kwargs)
        
class User(Base):
    """
    Represents a user of the system. 
    
    A User contains attributes that are common for any user of the system.
    Other attributes can be linked with a user using the UserField class
    """
    """Forename of the User"""
    forename = models.CharField(max_length=50)
    """Surname of the User"""
    surname = models.CharField(max_length=50)
    """Username or alias for the User object"""
    username = models.CharField(max_length=25)
    """Email address registered with the User"""
    email = models.EmailField(max_length=75)
    """Phone number for the User"""
    phone = models.CharField(max_length=20)
    
    def add_user_field(self, UserField):
        """
        Adds a UserField object to the User
        
        @param UserField The UserField object to set as belonging to the user.
        @return UserField Returns the UserField added. 
        @throws UserDataException
        """
        return
    
class UserField(Base):
    """
    A UserField is a value attached to a user.
    
    Users can have multiple UserFields allowing for unique fields
    to be added to a specific User.
    """
    """The User the UserField belongs to"""
    user = models.ForeignKey(User)
    """The field key"""
    key = models.CharField(max_length=250)
    """The field value"""
    value = models.TextField()

class Attachment(Base):
    """
    An Attachment is a collection of revisions. 
    
    Attachment objects can be used to derive a full file revision history, 
    and retrieve the original version of the file
    """
    
    """The title of the Attachment"""
    title = models.CharField(max_length=50)
    """The file name e.g file.pdf"""
    file_name = models.CharField(max_length=50)
    """The description of the Attachment"""
    description = models.CharField(max_length=250)
    """The User owning the Attachment, usually the uploader."""
    owner = models.ForeignKey(User)
    
    def get_total_size(self):
        """
        Returns the total size used of all revisions in the Attachment object.
        
        @return: Float A float of the total size in Kb
        """
        return
    
    def remove_revision(self, revision_uuid):
        """
        Removes the revision from the attachment with the 
        specified uuid.
        
        @param UUID The uuid of the revision to be purged.
        @return Revision The Revision object removed.
        """
        return
    
    def purge_revisions(self):
        """
        Purges all Revisions but the most recent in the Attachment object.
        """
        return
    
    def get_all_revisions(self):
        """
        Returns an ordered List of revisions for the Attachment based on time uploaded.
        
        @return List Returns a list of all Revisions sorted descending order.
        """
        
    def add_revision(self, revision):
        """
        Adds the supplied Revision object to the Attachment with current timestamp.
        
        @param Revision The Revision object to add to the Attachment
        @throws AttachmentException If Revision file type is invalid.
        """
        
class Revision(Base):
    """
    A revision object represents a single file that belongs to an Attachment.
    
    This class facilitates Attachment versioning
    """
    """The timestamp the document was uploaded/attached to the revision"""
    time_uploaded = models.DateTimeField(auto_now_add=True)
    """The Attachment object the Revision belongs to."""
    attachment = models.ForeignKey(Attachment)
    """#The File Object"""
    file = models.FileField(upload_to='/')
    """Whether or not the Revision has been approved"""
    approved = models.BooleanField()
    """The User whom owns the Revision - Usually the uploader."""
    uploaded_by = models.ForeignKey(User)
    """The file size of the Revision file."""
    file_size = models.FloatField()
    
    def get_file(self):
        """
        Returns the File object for the current Revision.
        @return File Returns the File handler for the Revision
        """
        return
    
class Link(Base):
    """
    Holds to a resource.
    
    Links can be added to many other Objects.
    """
    """The title for the Link story"""
    title = models.CharField(max_length=250)
    """The description of the Link"""
    description = models.TextField()
    """The Link URl in string form"""
    link = models.URLField(max_length=250)

class Video(Base):
    """
    Represents a video, can contain multiple VideoFormats.
    Contains video title, keywords and description.
    """
    title = models.CharField(max_length=50)
    description = models.TextField()
    
    def get_file_paths(self):
        """
        Returns a dictionary of filepaths for every availiable format
        """
        return
    
    def get_file_path(self, format):
        """
        Returns the video file path for the specified format
        """
        return
    
class VideoFormat(Base):
    """
    Repersents a specific format converted video file
    belongs to a video object
    """
    format = models.CharField(max_length=20)
    encoding = models.CharField(max_length=50)
    bitrate = models.CharField(max_length=10)
    file = models.FileField(upload_to='/')
    
    def probe(self):
        """Return ffprobe class from video."""
        return
    
class Lecture(Base):
    """
    Represents a lecture within a module.
    Contains details about an individual lecture & references to
    lecture content (Videos, Attachments and Lecture Notes).
    """
    title = models.CharField(max_length=50)
    videos = models.ManyToManyField(Video)
    attachments = models.ManyToManyField(Attachment)
    validFrom = models.DateField()
    validTo = models.DateField()
    visible = models.BooleanField(default=True)
    links = models.ManyToManyField(Link)
    lecturers = models.ManyToManyField(User)

    
class Module(Base):
    """
    A module belonging to a course
    """
    title = models.CharField(max_length=100)
    module_code = models.CharField(max_length=100)
    attachments = models.ManyToManyField(Attachment)
    lectures = models.ManyToManyField(Lecture)
    
class Course(Base):
    """
    A course represents a top level definition of a degree, they are a collection of modules
    """
    title = models.CharField(max_length=50)
    code = models.CharField(max_length=50)
    description = models.TextField()
    modules = models.ManyToManyField(Module)
    attachments = models.ManyToManyField(Attachment)
    
class Config(Base):
    """
    Contains configuration and preferences for the system.
    """
    key = models.CharField(max_length=250)
    data_type = models.CharField(max_length=10)
    value = models.TextField()
    
    
class Question(Base):
    """
    An instance of the Question class will hold the question string 
    with a List of answer objects that the user can pick.
    """
    content = models.TextField()
    type = models.CharField(max_length=40)
    
    def get_answers(self):
        """Returns the possible answers for the question"""
    
    def get_correct_answer(self):
        """Returns the correct answer for the question"""
        
        
class Test(Base):
    """
    An instance of the test class will contain details of the Test with the lecture it belongs to. 
    
    As well as the full set of questions that could be asked.
    """
    title = models.CharField(max_length=250)
    description = models.TextField()
    question_count = models.IntegerField()
    questions = models.ManyToManyField(Question)
    lecture = models.ManyToManyField(Lecture)
    
    def get_random_questions(self):
        """
        Returns a List of random questions taken from the property 
        QuestionList with the length of questionCount, 
        if questionCount is larger than the length of QuestionList a Exception will be thrown.
        """
        return
        
        
class Answer(Base):
    """
    An instance of the Answer class will hold text 
    associated with an answer, and whether or not the answer is correct or not.
    """
    content = models.CharField(max_length=250)
    correct = models.BooleanField()
    question = models.ForeignKey(Question)
    
class TestInstance(Base):
    """
    A TestInstance object contains a reference to related Test,
     the student completing it and the time it was completed
    """
    student = models.ForeignKey(User)
    test = models.ForeignKey(Test)
    time_completed = models.DateTimeField()
    
    def calc_result(self):
        """
        Returns the percentage of answers correct in the TestInstance as a float.
        """
        return
    
class Result(Base):
    """
    The result class stores a reference to the answer selected 
    for a single question in a test, belonging to a TestInstance.
    """
    test_instance = models.ForeignKey(TestInstance)
    question = models.ForeignKey(Question)
    answer = models.ForeignKey(Answer)
    

class EventLog(Base):
    """
    Handles the storing of events in the log
    """
    event_uuid = models.CharField(max_length=36)
    event_type = models.CharField(max_length=50)
    severity = models.CharField(max_length=50)
    content = models.TextField()
    timestamp = models.DateTimeField()
    

