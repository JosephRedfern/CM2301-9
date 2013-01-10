from django.db import models
import uuid

class Base(models.Model):
    """
    Base class containing common properties and methods for models.
    
    All models will extend this class.
    """
    
    """UUID of the object, as String"""
    uuid = models.CharField(max_length=36, primary_key=True)
    
    class Meta:
        app_label = "learn"
        abstract = True
    
    def save(self, *args, **kwargs):
        """
        Overrides the django.model.save() method to add a random UUID
        to new objects before they are persisted to the DB.
        """
        if not self.uuid:
            uuid = str(uuid.uuid4())
        super(Base, self).save(*args, **kwargs)
        
    def get_data_fields(self):
        """
        Returns any DataFields that are related to the object.
        @return DataField Returns any DataField objects associated with the object
        """
        return
        
    
        
        
################################################################
#Core System
################################################################
        
class User(Base):
    """
    Represents a user of the system. 
    
    A User contains attributes that are common for any user of the system.
    Other attributes can be linked with a user using the UserField class
    """
    ##Forename of the User
    forename = models.CharField(max_length=50)
    ##Surname of the User
    surname = models.CharField(max_length=50)
    ##Username or alias for the User object
    username = models.CharField(max_length=25)
    ##Email address registered with the User
    email = models.EmailField(max_length=75)
    ##Phone number for the User
    phone = models.CharField(max_length=20)
    
    def add_user_field(self, UserField):
        """
        Adds a UserField object to the User
        
        @param UserField The UserField object to set as belonging to the user.
        @return UserField Returns the UserField added. 
        @throws UserDataException
        """
        return
    
class DataField(Base):
    """
    A UserField is a value attached to another object.
    
    Objects can have multiple DataFields allowing for an extensiable Schema
    """
    ##The object uuid the datafield belongs to
    object_uuid = models.CharField(max_length=36)
    ##The field key
    key = models.CharField(max_length=250)
    ##The field value
    value = models.TextField()
    
################################################################
#File Handling
################################################################

class Attachment(Base):
    """
    An Attachment is a collection of revisions. 
    
    Attachment objects can be used to derive a full file revision history, 
    and retrieve the original version of the file
    """
    
    ##The title of the Attachment
    title = models.CharField(max_length=50)
    ##The file name e.g file.pdf
    file_name = models.CharField(max_length=50)
    ##The description of the Attachment
    description = models.CharField(max_length=250)
    ##The User owning the Attachment, usually the uploader.
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
    ##The timestamp the document was uploaded/attached to the revision
    time_uploaded = models.DateTimeField(auto_now_add=True)
    ##The Attachment object the Revision belongs to.
    attachment = models.ForeignKey(Attachment)
    ###The File Object
    file = models.FileField(upload_to='/')
    ##Whether or not the Revision has been approved
    approved = models.BooleanField()
    ##The User whom owns the Revision - Usually the uploader.
    uploaded_by = models.ForeignKey(User)
    ##The file size of the Revision file.
    file_size = models.FloatField()
    
    def get_file(self):
        """
        Returns the File object for the current Revision.
        @return File Returns the File handler for the Revision
        """
        return
    
################################################################
#Lecturing Classes
################################################################
    
class Link(Base):
    """
    Holds to a resource.
    
    Links can be added to many other Objects.
    """
    ##The title for the Link story
    title = models.CharField(max_length=250)
    ##The description of the Link
    description = models.TextField()
    ##The Link URl in string form
    link = models.URLField(max_length=250)

class Video(Base):
    """
    Represents a video, can contain multiple VideoFormats.
    
    Contains video title, keywords and description.
    """
    ##The title of the Video
    title = models.CharField(max_length=50)
    ##The description for the video
    description = models.TextField()
    
    def get_file_paths(self):
        """
        Returns a dictionary of filepaths for every availiable format
        
        @return Dict Returns a dictionary of format:filepath
        """
        return
    
    def get_file_path(self, format):
        """
        Returns the video file path for the specified format
        
        @return String A string of the Format filepath
        """
        return
    
class VideoFormat(Revision):
    """
    Represents a specific video format containing a file.
    
    Belongs to a video object.
    """
    ##The container format as a string. e.g .ogg
    format = models.CharField(max_length=20)
    ##The encoding used for the video. e.g H.264
    encoding = models.CharField(max_length=50)
    ##The bitrate of the video
    bitrate = models.CharField(max_length=10)
    ##The Video object the format belongs to.
    video = models.ForeignKey(Video)
    
    def probe(self):
        """
        Return ffprobe class from video.
        
        Gets details about the video file using FFPROBE
        
        @return: ffprobe 
        """
        return
    
class Lecture(Base):
    """
    Represents a lecture in the system.
    
    Contains details about an individual lecture & references to
    lecture content (Videos, Attachments and Lecture Notes).
    """
    ##The title of the lecture
    title = models.CharField(max_length=50)
    ##The videos used in the lecture
    videos = models.ManyToManyField(Video)
    ##Attachments to be presented with the lecture
    attachments = models.ManyToManyField(Attachment)
    ##The date the Lecture becomes valid.
    validFrom = models.DateField()
    ##The date the lecture expires.
    validTo = models.DateField()
    ##Whether the lecture is visible
    visible = models.BooleanField(default=True)
    ##Links that may be useful.
    links = models.ManyToManyField(Link)
    ##Lecturers who teach the lecture. - They should be in the module lecturers.
    lecturers = models.ManyToManyField(User)
    
class Module(Base):
    """
    A module is a set of lectures belonging to multiple courses.
    
    Modules can share Lecture objects, Module objects can belong
    to multiple Course objects.
    """
    ##The title of the Module. E.g Python
    title = models.CharField(max_length=100)
    ##The module code - CM2103
    module_code = models.CharField(max_length=100)
    ##Attachments linked to the module obejct
    attachments = models.ManyToManyField(Attachment)
    ##The lectures used in the module
    lectures = models.ManyToManyField(Lecture)

class Course(Base):
    """
    A course represents a top level definition of a degree. 
    
    Contains a collection of modules
    """
    ##The title of the course
    title = models.CharField(max_length=50)
    ##The course code it holds e.g G400
    code = models.CharField(max_length=50)
    ##The description of the course
    description = models.TextField()
    ##The modules which are in the course
    modules = models.ManyToManyField(Module)
    ##Attachments attached to the course. E.g Timetable
    attachments = models.ManyToManyField(Attachment)
    
    def get_lectures(self):
        """
        Returns a list of all Lecture objects in this course.
        @return List Returns a list of Lecture objects.
        """
    
    
################################################################
#Testing/Marking Classes
################################################################

class Question(Base):
    """
    An instance of the Question class holds the question string
    with a List of answer objects that the user can pick.
    """
    ##The question text - Can be any format.
    content = models.TextField()
    ##The type of question - e.g Multiple Choice
    type = models.CharField(max_length=40)
    
    def get_answers(self):
        """
        Returns the possible answers for the question
        @return List Returns all Answer objects for the Question
        """
    
    def get_correct_answer(self):
        """
        Returns the correct Answer for the question
        
        @return Answer Returns the correct Answer object
        @throws TestException If no correct Answer found.
        """
        
        
class Test(Base):
    """
    An instance of the test class will contain details of the Test with the lecture it belongs to. 
    
    As well as the full set of questions that could be asked.
    """
    ##The title of the Test
    title = models.CharField(max_length=250)
    ##The description of the Test
    description = models.TextField()
    ##The number of questions to be presented to the user
    question_count = models.IntegerField()
    ##The questions from which they will be randomly selected.
    questions = models.ManyToManyField(Question)
    ##The lectures the test belong to.
    lecture = models.ManyToManyField(Lecture)
    
    def get_random_questions(self):
        """
        Returns a List of random questions taken from the
        QuestionList with the length of questionCount, 
        if questionCount is larger than the length of QuestionList a Exception will be thrown.
        
        @return List Returns a list of Question objects
        @throws TestException
        """
        return
        
        
class Answer(Base):
    """
    An instance of the Answer class hold answer details.
     
    Associated with an Question, and whether or not the answer is correct or not.
    """
    ##The answer text
    content = models.CharField(max_length=250)
    ##Whether or not the question is correct
    correct = models.BooleanField()
    ##The question the 
    question = models.ForeignKey(Question)
    
class TestInstance(Base):
    """
    A TestInstance object contains a reference to related Test,
     the student completing it and the time it was completed
    """
    ##The User who completed the Test
    student = models.ForeignKey(User)
    ##The associated Test object.
    test = models.ForeignKey(Test)
    ##The time the Test was completed.
    time_completed = models.DateTimeField()
    
    def calc_result(self):
        """
        Returns the percentage of answers correct in the TestInstance as a float.
        
        @return Float Returns mark as a percentage
        """
        return
    
class Result(Base):
    """
    The result class stores a reference to the answer selected 
    for a single question in a test, belonging to a TestInstance.
    """
    ##The Test instance the result set belongs to
    test_instance = models.ForeignKey(TestInstance)
    ##The question answered
    question = models.ForeignKey(Question)
    ##The answer chosen
    answer = models.ForeignKey(Answer)

################################################################
#Coursework Setting/Marking Classes
################################################################

class CourseworkTask(Base):
    """
    Represents a coursework attached to a module.
    
    Holds details on how to complete/submit the coursework.
    """
    ##The titel of the coursework task
    title = models.CharField(max_length=250)
    ##The coursework instructions
    content = models.TextField()
    ##Any attachments associated with the coursework
    attachments = models.ManyToManyField(Attachment)
    ##The module the coursework belongs to
    module = models.ManyToManyField(Module)
    ##The coursework start date
    start_date = models.DateTimeField()
    ##The coursework submission date
    due_date = models.DateTimeField()
    
class ProgrammingTask(CourseworkTask):
    """
    ProgrammingTask extends CourseworkTask, facilitating for autmation of marking.
    
    Allows the user to create a ProgrammingTask object which is subject
    to automated marking.
    """
    ##The language used for the assessment
    language = models.CharField(max_length=20)
    ##The input and expected output to test the code
    input_output = models.TextField()
    
    
class CourseworkSubmission(Base):
    """
    CourseworkSubmission caters for the submission of coursework by a user.
    
    A CourseworkSubmission object contains details of uploaded files and
    CourseworkTask.
    """
    ##The User submitting the coursework
    student = models.ForeignKey(User)
    ##The coursework attachments/uploads
    attachments = models.ManyToManyField(Attachment)
    ##The related CourseworkTask
    courswork_task = models.ForeignKey(CourseworkTask)
    ##The mark recieved by the student
    score = models.FloatField()
    ##Whether the CourseworkSubmission has been marked
    marked = models.BooleanField()
    
    def set_marked(self):
        """
        Sets the marked attribute to be True
        """
        return
    
    def set_unmarked(self):
        """
        Sets the marked attribute to be False
        """
        return

class ProgrammingSubmission(CourseworkSubmission):
    """
    The ProgrammingSubmission class extends the CourseworkSubmission Class.
    
    Allows for automated marking of programming based courseworks.
    """
    ##The files to be run
    scripts = models.ManyToManyField(Attachment)
    ##The main entry point to the program e.g main.py
    main = models.CharField(max_length=200)
    ##Flag whether to extract zip files.
    extract_compressed = models.BooleanField()
    
    
################################################################
#System Maintainence Classes
################################################################

class EventLog(Base):
    """
    Handles the storing of events in the log
    
    This class handles logging accross the system, if debugging 
    is enabled everything will be dumped.
    """
    ##The UUID of the object in question
    event_uuid = models.CharField(max_length=36)
    ##The type of event, e.g created, exception etc
    event_type = models.CharField(max_length=50)
    ##The severity of the logged event
    severity = models.CharField(max_length=50)
    ##Any content of the event
    content = models.TextField()
    ##The timestamp of the event
    timestamp = models.DateTimeField()
    
class Config(Base):
    """
    Contains configuration and preferences for the system.
    
    This class stores configuration and system wide preferences.
    """
    ##The key for the preference e.g stylesheet
    key = models.CharField(max_length=250)
    ##The type of data the value is stored as e.g xml
    data_type = models.CharField(max_length=10)
    ##The config value
    value = models.TextField()
    
class Server(Base):
    """
    A Server represents a single server in a server farm configuration.
    
    Attributes of this class are utilised to aid in load balancing
    """
    ##The alias of the server
    alias = models.CharField(max_length=250)
    ##The server hostname as an IP. 10.0.0.3
    hostname = models.GenericIPAddressField()
    ##The operating system of the server
    os = models.CharField(max_length=250)
    ##The server private key for executing ssh
    private_key = models.TextField()
    ##The role of the Server in the serverfarm
    role = models.CharField(max_length=30)
    ##The last updated load on server
    load = models.FloatField()
    ##The amount of free disk storage on the server
    free_storage = models.FloatField()
    
    
class QueueItem(Base):
    """
    QueueItem is responsible for handling load balancing of CPU/Memory intensive tasks.
    
    If multiple servers are added to the system then they will poll for jobs to take
    """
    ##The job type 
    job_type = models.CharField(max_length=30)
    ##The UUID of the object the job relates to
    item_uuid = models.CharField(max_length=32)
    ##The time the QueueItem was created.
    submission_time = models.DateTimeField()
    ##Whether the job is pending
    pending = models.BooleanField()
    ##Progress of the job, as a percentage
    progress = models.FloatField()
    ##The time of job completion
    completion_time = models.DateTimeField()

