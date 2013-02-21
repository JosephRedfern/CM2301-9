from django.forms import ModelForm
from learn.models import *
from django.forms import ModelForm, DateInput

class VideoUploadForm(ModelForm):
    class Meta:
        model = Video
        
class LectureCreateForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ('id', 'visible')
        widgets = {
            'validFrom': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yy'}),
            'validTo': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yy'}),
        }