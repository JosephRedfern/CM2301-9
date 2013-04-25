"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from models import Attachment
class AttachmentTestCase(TestCase):
    """
    A test class for Attachment
    """

    def setUp(self):
            self.file1 = Attachment(file_name="file1", description="A file")
            self.file2 = Attachment(file_name="file2", description="Another File")

    def test_get_total_size(self):
            """
            The File Size is determined
            """
            self.assertEqual(self.file1.get_total_size(), 0)
            self.assertEqual(self.file2.get_total_size(), 0)

    def test_remove_revision(self, revision_uuid):

    def test_purge_revisions(self):

    def test_get_all_revisions(self):

    def test_add_revision(self, revision):

    def test_get_absolute_url(self):

    def test_compress_revisions(self, method='zip'):

    def test_get_latest_revision(self):

    def test_mimetype(self):

class ViewedTestCase(TestCase):
    def setUp(self):

    def test_log_view(cls, request, object_id):

class User(TestCase):
    def setUp(self):

    def test_add_user_field(self, UserField):

class BaseTestCase(TestCase):
    def setUp(self):

    ## Should I do this??
    ## 
    ## Is it required? 

class UserTestCase(TestCase):
    def setUp(self):

    def test_add_user_field(self, UserField):

class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)

class CourseworkSubmissionTestCase(TestCase):
    def setUp(self):

    def test_set_marked(self):

    def test_set_unmarked(self):

class TestInstanceTestCase(TestCase):
    def setUp(self):

    def test_calc_result(self):

class TestTestCase(TestCase):
    def setUp(self):

    def test_get_random_questions(self):

class QuestionTestCase(TestCase):
    def setUp(self):

    def test_get_answers(self):

    def test_get_correct_answer(self):

class CourseTestCase(TestCase):
    def setUp(self):

    def test_get_lectures(self):

class LectureTestCase(TestCase):
    def setUp(self):

    def test_get_absolute_url(self):

class ModuleTestCase(TestCase):
    def setUp(self):

    def test_get_absolute_url(self):

class VideoFormatTestCase(TestCase):
    def setUp(self):

    def test_probe(self):

    def test_get_absolute_url(self):

class VideoThumbnailTestCase(TestCase):
    def setUp(self):

    def test_get_absolute_url(self):

class VideoTestCase(TestCase):
    def setUp(self):

    def test_save(self, *args, **kwargs):

    def test_get_file_paths(self):

    def test_get_file_path(self, format):

    def test_url(self):

    def test_convert(self):

    def test_generate_thumbnails(self, thumbnail_count, size):

    def test_update_progress(self, converters):

    def test_save(self, *args, **kwargs):

class Revision(TestCase):
    def setUp(self):

        self.file1 = Attachment(file_name="file1", description="A file")
        self.file2 = Attachment(file_name="file2", description="Another File")

        self.revision1 = Revision(version="1", )
        self.revision2 = 

    def test_filename(self):

    def test_get_file(self):

    def test_save(self):

    def test_get_absolute_url(self):

    def test_get_version_filename(self):
        self.assertEqual(self.revision1.get_version_filename(), str(1) + "_" os.path.basename(self.file.name))
    def test_clean(self):

    def test_mimetype(self):
