from django.forms import ModelForm, Form
from django import forms
from learn.models import *
from django.forms import ModelForm, DateInput

class AttachmentForm(ModelForm):
    class Meta:
        model = Attachment

class TestForm(forms.Form):
    def initialise(self, questions):
        for question in questions:
            choices = [(choice.id, choice.content) for choice in Answer.objects.filter(question=question.id)]
            self.fields["%s"%(question.id)] = forms.ChoiceField(choices, widget=forms.RadioSelect(), label=question.content)

    class Meta:
        model = Test

class VideoForm(ModelForm):
    class Meta:
        model = Video
        fields = ('uploaded_video',)
        
class LectureForm(ModelForm):
    class Meta:
        model = Lecture
        exclude = ('id', 'visible', 'video')
        widgets = {
            'valid_to': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yy'}),
            'valid_from': DateInput(attrs={'class': 'datepicker', 'data-date-format': 'dd/mm/yy'}),
        }
        
class RevisionForm(ModelForm):
    class Meta:
        model = Revision
        #fields = ('file',)
        
class CreateFAQQuestionForm(ModelForm):
    class Meta:
        model = FAQQuestion

class CreateFAQAnswerForm(ModelForm):
    class Meta:
        model = FAQAnswer