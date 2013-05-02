"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from models import Attachment, Viewed, User, CourseworkSubmission, TestInstance, Question, Course, Lecture, Module, VideoFormat, VideoThumbnail, Video, Revision

################################################################
#File Handling
################################################################

class AttachmentTestCase(TestCase):
    """
    A test class for Attachment
    """

    def setUp(self):
            self.file1 = Attachment(file_name="file1", description="A file", object_id="d636abe0-b293-11e2-9e96-0800200c9a66")
            self.file2 = Attachment(file_name="file2", description="Another File", object_id="d636abe0-b293-11e2-9e96-0800200c9a66")

            revision_uuid="d636abe0-b293-11e2-9e96-0800200c9a66"

    def test_get_total_size(self):
        """
        The File Size is determined
        """
        self.assertEqual(self.file1.get_total_size(), 0)
        self.assertEqual(self.file2.get_total_size(), 0)

    def test_remove_revision(self):
        """
        To remove revision, a revision is returned 
        """
        self.assertEqual(self.file1.remove_revision(self.file1.object_id), self.file1)
        self.assertEqual(self.file2.remove_revision(self.file2.object_id), self.file2)

    def test_get_all_revisions(self):
        """
            ???
        """

    def test_get_absolute_url(self):
        """
            Need to understand reverse
        """

    def test_compress_revisions(self, method='zip'):
        """
        """

class RevisionTestCase(TestCase):
    def setUp(self):

        self.file1 = Attachment(file_name="file1", description="A file")
        self.file2 = Attachment(file_name="file2", description="Another File")

        self.revision1 = Revision(version="1", )
        ##self.revision2 = 

    def test_filename(self):
        """
        """
    def test_get_file(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """
    def test_get_version_filename(self):
        """
        """
        ##self.assertEqual(self.revision1.get_version_filename(), str(1) + "_" os.path.basename(self.file.name))

################################################################
#Lecturing Classes
################################################################

class VideoTestCase(TestCase):
    def setUp(self):
        """
        """

    def test_get_file_paths(self):
        """
        """
    def test_get_file_path(self, format):
        """
        """
    def test_url(self):
        """
        """
    def test_convert(self):
        """
        """
    def test_save(self, *args, **kwargs):
        """
        """

class VideoThumbnailTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """

class VideoFormatTestCase(TestCase):
    def setUp(self):
        """
        """

    def test_get_absolute_url(self):
        """
        """

class FAQQuestionTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """

class FAQAnswerTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """

class ModuleTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """

class LectureTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_absolute_url(self):
        """
        """

################################################################
#Testing/Marking Classes
################################################################

class TestTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_get_random_questions(self):
        """
        """

class TestInstanceTestCase(TestCase):
    def setUp(self):
        self.testInstance1 = TestInstance()

    def test_calc_result(self):
        """
        """
    
    def test_get_absolute_url(self):
        """
        """

################################################################
#Coursework Setting/Marking Classes
################################################################

class CourseworkTaskTestCase(TestCase):
    def setUp(self):
        """
        """

    def test_get_absolute_url(self):
        """
        """

class CourseworkSubmissionTestCase(TestCase):
    def setUp(self):
        """
        """
    def test_set_marked(self):
        """
        """
    def test_set_unmarked(self):
        """
        """

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)











