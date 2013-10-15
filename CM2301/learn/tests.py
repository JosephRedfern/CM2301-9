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
            """
            """
    def test_get_total_size(self):
        """
        The File Size is determined
        """
        self.assertEqual(self.file1.get_total_size(), 0)
        self.assertEqual(self.file2.get_total_size(), 0)

class RevisionTestCase(TestCase):
    def setUp(self):

        ##self.file1 = Attachment(file_name="file1", description="A file")
        ##self.file2 = Attachment(file_name="file2", description="Another File")

        #self.revision1 = Revision(version="1", )
        ##self.revision2 = 
        self.revision1 = Attachment(file_name="rev123")
        self.revision2 = Attachment(file_name="rev1234")
        """
        """
    def test_filename(self):

            self.assertEqual(self.revision1.file_name, "rev123")
            self.assertEqual(self.revision2.file_name, "rev1234")

    def test_get_file(self):
        """
        """

    def test_get_version_filename(self):
        self.assertEqual(self.revision1.file_name, "rev123")
        ##self.assertEqual(self.revision1.get_version_filename(), str(1) + "_" os.path.basename(self.file.name))


################################################################
#Testing/Marking Classes
################################################################

class TestTestCase(TestCase):
    def setUp(self):
        """
        """
        self.question = Question.objects.get(content="Question1")
        self.test1 = Test(title="MyTest", questions=self.question)

    def test_get_random_questions(self):
        """
        """
        self.assertEqual(self.test1.get_random_questions(), "Question1")

class TestInstanceTestCase(TestCase):
    def setUp(self):
        self.testInstance1 = TestInstance(test_score="100")

    def test_calc_result(self):
        """
        """
        self.assertEqual(self.testInstance1.test_score, "100")

################################################################
#Coursework Setting/Marking Classes
################################################################

class CourseworkSubmissionTestCase(TestCase):
    def setUp(self):
        """
        """
        self.user = User.objects.get(username="geraint")
        self.coursework1 = CourseworkSubmission(marked=True, student=self.user)
        self.coursework2 = CourseworkSubmission(marked=True, student=self.user)

    def test_set_marked(self):
        """
        """
        self.assertEqual(self.coursework1.set_marked(), True)
        self.assertEqual(self.coursework2.set_marked(), True)
    def test_set_unmarked(self):
        """
        """
        self.assertEqual(self.coursework1.set_marked(), True)
        self.assertEqual(self.coursework2.set_marked(), True)










