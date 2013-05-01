from django.forms import ModelForm, Form
from django import forms
from django.contrib import messages
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


class ModuleAssociateForm(forms.Form):
    modules = forms.ModelChoiceField(queryset = Module.objects.all())


class CourseworkSubmissionForm(forms.Form):
    submission = forms.FileField(
        label='Select a file',
        )