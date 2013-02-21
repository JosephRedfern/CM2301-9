from django.forms import ModelForm
from learn.models import *

class VideoUploadForm(ModelForm):
    class Meta:
        model = Video
        
class LectureCreateForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ('id', 'visible')