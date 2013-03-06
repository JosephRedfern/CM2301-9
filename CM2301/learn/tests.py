"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""
from django.utils import unittest
from django.test import TestCase
from models import Attachment
class AttachmentTestCase(unittest.TestCase):
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


class SimpleTest(TestCase):
    def test_basic_addition(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEqual(1 + 1, 2)
