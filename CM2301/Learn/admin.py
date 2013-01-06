from models import *
from django.contrib import admin

ms = [User, UserField, Attachment, Revision, Link, Video, Module, Lecture]

for m in ms:
    admin.site.register(m)
