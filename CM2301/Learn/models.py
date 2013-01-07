from django.db import models
import uuid

class Base(models.Model):
    
    uuid = models.CharField(max_length=36, primary_key=True)
    
    def save(self, *args, **kwargs):
        if not self.uuid:
            uuid = str(uuid.uuid4())
        super(Base, self).save(*args, **kwargs)
        
class User(Base):
    """
    Represents any user of the system. 
    A User contains attributes that are common for any user of the system.
    """
    forename = models.CharField(max_length=50)
    surname = models.CharField(max_length=50)
    username = models.CharField(max_length=25)
    email = models.EmailField(max_length=75)
    phone = models.CharField(max_length=20)
    
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
    
    ##The title of the attachment
    title = models.CharField(max_length=50)
    ##The file name e.g file.pdf
    file_name = models.CharField(max_length=50)
    ##The description of the attachment
    description = models.CharField(max_length=250)
    ##
    #@property Owner 
    #@type User User
    ##
    owner = models.ForeignKey(User)
    
    def get_total_size(self):
        """
        Returns the total size used of all revisions
        @param self: FUCKING SELF
        """
        return
    
    def remove_revision(self, revision_uuid):
        """
        Removes the revision from the attachment with the 
        specified uuid.
        @param self: FUCKING SELF
        @param uuid: The uuid of the revision 
        
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
    time_uploaded = models.DateTimeField(auto_now_add=True)
    attachment = models.ForeignKey(Attachment)
    file = models.FileField(upload_to='/')
    approved = models.BooleanField()
    uploaded_by = models.ForeignKey(User)
    file_size = models.FloatField()
    
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
    

