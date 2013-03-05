from django.db import models
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from uuidfield import UUIDField
from django.core.urlresolvers import reverse
import tempfile, zipfile, os, tarfile, StringIO, mimetypes
from django.core.exceptions import ValidationError

class Base(models.Model):
    """
    Base class containing common properties and methods for models.
    
    All models will extend this class.
    """
    
    """UUID of the object, as String"""
    id = UUIDField(auto=True, primary_key=True)
    _attachments = None
    _custom_fields = None
    _links = None
    
    class Meta:
        app_label = "learn"
        abstract = True
        
    @property
    def attachments(self):
        """
        The getter method for Attachments, will retrieve all attachments
        associated with the object.
        """
        if (self._attachments is None):
            self._attachments = list(Attachment.objects.filter(object_id = self.id))
        return self._attachments
    
    
    @property
    def custom_fields(self):
        """
        Getter method for CustomField, will return all associated CustomField
        objects.
        """
        if (self._custom_fields is None):
            self._custom_fields = list(CustomField.objects.filter(object_id = self.id))
        return self._custom_fields
    
    @property
    def links(self):
        """
        Returns all links associated with the current CustomField
        """
        if (self._links is None):
            self._links = list(Links.objects.filter(object_id = self.id))
        return self._links
    
    def save(self, *args, **kwargs):
        """
        Overrides the django.model.save() method to add a random UUID
        to new objects before they are persisted to the DB.
        
        Also iterates through Attachments and CustomFields, persisting changes.
        """
        if self._attachments is not None:
            for attachment in self._attachments:
                attachment.save()
        if self._custom_fields is not None:
            for cf in self._custom_fields:
                cf.save()
        super(Base, self).save(*args, **kwargs)
        
        
    def get_custom_fields(self):
        """
        Returns any CustomField objects that are related to the object.
        @return CustomField Returns any CustomField objects associated with the object as a list.
        """
        return CustomField.objects.filter(object_id=self.id)
    
    def set_custom_field(self, data_type, key, value):
        """
        Uses the supplied paramaters to create a custom field
        and attach it to the object.

        @param data_type The datatype of the custom field.
        @param key The CustomField key.
        @param value The value of the field.
        
        @return CustomField Returns the created CustomField object. 
        """
        
    def add_custom_field(self, custom_field):
        """
        Sets the supplied CustomField object to the object.
        @param CustomField The CustomField object to set. 
        """
        
        
################################################################
#Core System
################################################################
             
        
class User(AbstractUser, Base):
    """
    Represents a user of the system. 
    
    A User contains attributes that are common for any user of the system.
    Other attributes can be linked with a user using the UserField class
    """
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
    
    def __unicode__(self):
        return self.username
    
class CustomField(Base):
    """
    A CustomField is a value attached to another object.
    
    This allows for a much more flexible model.
    Objects can have multiple CustomField allowing for an extensiable Schema
    """
    ##The object uuid the datafield belongs to
    object_id = UUIDField()
    ##The datatype of the field, it will be converted back.
    data_type = models.CharField(max_length=15)
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
    ##Object UUID - The UUID of the owning object.
    object_id = UUIDField()
    ##The file name e.g file.pdf
    file_name = models.CharField(max_length=50)
    ##The description of the Attachment
    description = models.CharField(max_length=250)
    ##The User owning the Attachment, usually the uploader.
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
    
    def get_total_size(self):
        """
        Returns the total size used of all revisions in the Attachment object.
        
        @return: Float A float of the total size in Kb
        """
        revisions = self.revision_set.all()

        total_size = 0
        for revision in revisions:
            total_size += revision.file_size

        return total_size

    def remove_revision(self, revision_uuid):
        """
        Removes the revision from the attachment with the 
        specified uuid.
        
        @param UUID The uuid of the revision to be purged.
        @return Revision The Revision object removed.
        """
        revision = Revision.objects.get(uuid = revision_uuid)
        revision.delete()
        return revision #this might cause issues... we'll see. not sure if .delete() also deletes the object from memory. 
    
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
        return Revision.objects.order_by('time_uploaded')
        
    def add_revision(self, revision):
        """
        Adds the supplied Revision object to the Attachment with current timestamp.
        
        @param Revision The Revision object to add to the Attachment
        @throws AttachmentException If Revision file type is invalid.
        """
        
    def get_absolute_url(self):
        return reverse('learn.views.attachment.attachment', args=[str(self.id)])

    def __unicode__(self):
        return self.file_name
    
    def compress_revisions(self, method='zip'):
        """
        Returns a temporary file object of a zip file containing every revision
        belonging to the attachment. Directory can be found using tmp.name
        
        @return NamedTemporaryFile Temp file of the zip. 
        """
        
        tmp = tempfile.NamedTemporaryFile(delete=False)
        if method is 'zip':
            z = zipfile.ZipFile(tmp, 'w', zipfile.ZIP_DEFLATED)
            for revision in self.revision_set.all():
                z.write(revision.file.file.name, revision.get_version_filename())
            z.close()
        elif method is 'gz':
            tar = tarfile.open(tmp.name, "w:gz")
            for revision in self.revision_set.all():
                tar.add(revision.file.file.name, arcname=revision.get_version_filename())
            tar.close()
            
        tmp.seek(0)
        return tmp
    
    def get_latest_revision(self):
        return self.revision_set.all()[0]
    
    def mimetype(self):
        """
        Returns the mimetype of the attachment file as a string.
        For example "video/mp4"
        """
        type = mimetypes.guess_type(self.file_name)
        return type[0]
        
        
        

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
    file = models.FileField(upload_to='attachments')
    ##Whether or not the Revision has been approved
    approved = models.BooleanField()
    ##The User whom owns the Revision - Usually the uploader.
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    ##The file size of the Revision file.
    file_size = models.FloatField(null=True, blank=True)
    ##The version number of the revision
    version = models.IntegerField(null=True, blank=True)
    
    @property
    def filename(self):
        """
        Returns the actual filename of the file, as opposed to the relative path
        """
        return os.path.basename(self.file.name)
    
    def get_file(self):
        """
        Returns the File object for the current Revision.
        @return File Returns the File handler for the Revision
        """
        return self.file.file
    
    def save(self, *args, **kwargs):
        if self.file_size is None:
            self.file_size = self.file.size
            
        if self.version is None:
            self.version = len(self.attachment.revision_set.all()) + 1
        super(Revision, self).save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('learn.views.attachment.revision', args=[str(self.id)])
    
    
    def get_version_filename(self):
        """
        Returns the filename prefixed with the version number,
        Useful for when displaying revision history or downloading
        multiple revisions.
        
        e.g.  1_revision.pdf, 2_reivision.pdf
        @return String Returns a string of the filename
        """
        return str(self.version) + "_" + os.path.basename(self.file.name)
    
    def clean(self):
        """
        Ensures all validation passes before the object is saved
        """
        print self.filename
        print self.attachment.file_name
        if self.mimetype() != self.attachment.mimetype():
            raise ValidationError('Revisions must have the same filename as the attachment')
        
    def mimetype(self):
        """
        Returns the mimetype of the attachment file as a string.
        For example "video/mp4"
        """
        type = mimetypes.guess_type(self.file.name)
        return type[0]
    
    class Meta:
        get_latest_by = "time_uploaded"
        ordering = ['-version']
    
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
    
    def save(self, *args, **kwargs):
        super(Video, self).save(*args, **kwargs)
    
    uploaded_video = models.FileField(upload_to='videos')
    def get_file_paths(self):
        """
        Returns a dictionary of filepaths for every availiable format

        @return Dict Returns a dictionary of format:filepath
        """
        
        videoFormats = VideoFormat.objects.get(video=self)
        filePaths = {}
        for videoFormat in videoFormats:
            filePaths[videoFormat.encoding] = videoFormat.name #RELATIVE path.
        
        return filePaths
    
    def get_file_path(self, format):
        """
        Returns the video file path for the specified format
        
        @return String A string of the VideoFormat filepath
        """
        videoFormat = VideoFormat.objects.get(video=self, encoding=format)
        return videoFormat.name
    
    @property
    def url(self):
        """
        Returns the video original video file url
        """
        return settings.MEDIA_ROOT + os.sep + self.uploaded_video.url
        
    def convert(self):
        c.set_video_codec(VideoCodec.VP8)
        c.set_audio_codec('aac')
        c.set_container(ContainerFormat.MP4)
        c.set_dimensions(height=480)
        c.start()
        return c
    
class VideoThumbnail(models.Model):
    """
    Handles the storage of video thumbnails. 
    
    Thumbnails will be generated upon video being uploaded.
    """
    
    ##How many seconds into the video the thumbnail is.
    time = models.FloatField()
    ##The video the thumbnail belongs to.
    video = models.ForeignKey(Video)
    ##The thumbnail image.
    thumbnail = models.FileField(upload_to='thumbnails')
    
    def __unicode__(self):
        return "Thumbnail for " + self.video.__unicode__() + " at " + str(self.time) + "s"

    class Meta:
        ordering = ['time']
    
    
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

    def __unicode__(self):
        return self.video.__unicode__() + " in " + self.encoding
    
    
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
    attachments = models.ManyToManyField(Attachment, blank=True, null=True)

    description = models.CharField(max_length=8192)

    def __unicode__(self):
        return self.title + " (" + self.module_code + ")"

class Lecture(Base):
    """
    Represents a lecture in the system.
    
    Contains details about an individual lecture & references to
    lecture content (Videos, Attachments and Lecture Notes).
    """
    ##The title of the lecture
    title = models.CharField(max_length=50)
    ##The description of the lecture
    description = models.TextField()
    ##Attachments to be presented with the lecture
    attachments = models.ManyToManyField(Attachment, null=True, blank=True)
    ##The date the Lecture becomes valid.
    valid_from = models.DateField()
    ##The date the lecture expires.
    valid_to = models.DateField()
    ##Whether the lecture is visible
    visible = models.BooleanField(default=True)
    ##Links that may be useful.
    links = models.ManyToManyField(Link, null=True, blank=True)
    ##Lecturers who teach the lecture. - They should be in the module lecturers.
    lecturers = models.ManyToManyField(settings.AUTH_USER_MODEL)
    ##Module that this lecture is associated with
    module = models.ForeignKey(Module)
    ##Video that this lecture is associated with.
    video = models.ForeignKey(Video)

    def __unicode__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('learn.views.lecture.view', args=[str(self.id)])

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

    def __unicode__(self):
        return self.title + " (" + self.code + ")"
    
    
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

    def __unicode__(self):
        return self.content[:97]+"..."
        
        
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

    def __unicode__(self):
        return self.title
        
        
class Answer(Base):
    """
    An instance of the Answer class hold answer details.
     
    Associated with an Question, and whether or not the answer is correct or not.
    """
    ##The answer text
    content = models.CharField(max_length=250)
    ##Whether or not the question is correct
    correct = models.BooleanField()
    ##The question the answer is associated with
    question = models.ForeignKey(Question)
    
    def __unicode__(self):
        return self.content[:100]+"..."

class TestInstance(Base):
    """
    A TestInstance object contains a reference to related Test,
     the student completing it and the time it was completed
    """
    ##The User who completed the Test
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
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
    
    def __unicode__(self):
        return "Instance of "+self.test.__unicode__()+" for user "+self.student.__unicode__()

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

    def __unicode__(self):
        return "Answer to "+self.question


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

    def __unicode__(self):
        return "Coursework Task: "+self.title
    
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
    student = models.ForeignKey(settings.AUTH_USER_MODEL)
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
        self.marked = True
        self.save()
        return True
    
    def set_unmarked(self):
        """
        Sets the marked attribute to be False
        """
        self.marked = False
        self.save()
        return True

    def __unicode__(self):
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
    
class UserQuestion(Base):
    """
    Handles the User questioning system for an Object.
    
    The UserQuestion class allows for a Lecture, Module or CourseWorkTask to have 
    Questions and Answers attached to them. This will ensure students maintain 
    contact with the lecturers.
    """
    ##The UUID of the object the question is attached to.
    object_id = UUIDField()
    ##The title of the Question
    title = models.CharField(max_length=250)
    ##The question text.
    text = models.TextField()
    ##The User which posted the UserQuestion
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    ##The TimeDate of the post submission
    post_date = models.DateTimeField(auto_now_add=True)
    ##Whether the Question has been approved by a User
    approved = models.BooleanField(default=False)
    ##Whether the question is still open to more responses.
    closed = models.BooleanField(default=False)
    
    def get_responses(self):
        """
        Returns the QuestionResponse objects associated with the UserQuestion as a list.
        
        @return list Returns a list of QuestionResponse objects.
        """
        return
    
    def set_approved(self):
        """
        Sets the QuestionReponse object as being approved by a lecturer.
        """
        return


class QuestionResponse(Base):
    """
    QuestionReponse class handles the answering of UserQuestion objects.
    
    Multiple QuestionResponse objects can be attached to a single UserQuestion.
    """
    ##The parent UserQuestion object
    question = models.ForeignKey(UserQuestion)
    ##The answer text
    text = models.TextField()
    ##The date it was posted.
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    ##The user who posted it.
    post_date = models.DateTimeField(auto_now_add=True)
    
    
class Search(object):
    """
    This Search class handles the searching of objects in the database.
    
    The Search class will handle searching of objects in the database when passed a string.
    """
    
    ##The list of strings to search against.
    queries = []
    
    def add_search_string(self, string):
        """
        This method adds a string to the query list.
        """
        return
    
    def run_search(self):
        """
        Runs the search with supplied queries.
        @returns Dictionary Retuns a dictionary of matching object types.
       """

class Announcement(Base):
    """
    The announcements class handles the storing of Announcements.

    Title, Body, Valid From, Valid Until and Owner can all be specified.
    """
    title = models.CharField(max_length=256)
    body = models.TextField(max_length=4096)
    valid_from = models.DateTimeField(auto_now_add=True)
    valid_until = models.DateTimeField()
    owner = models.ForeignKey(settings.AUTH_USER_MODEL)
