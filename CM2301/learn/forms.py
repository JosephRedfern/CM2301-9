from django.forms import ModelForm
from learn.models import Video

class VideoUploadForm(ModelForm):
    class Meta:
        model = Video