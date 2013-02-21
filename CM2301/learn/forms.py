from django.forms import ModelForm
from learn.models import Video

class VideUploadForm(ModelForm):
    class Meta:
        model = Video