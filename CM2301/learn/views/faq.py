from django.shortcuts import render
from learn.models import *
from learn.forms import *
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView


@login_required
def faqs(request, module_id):
    values = dict()
    values['module'] = Module.objects.get(pk=module_id)
    values['lectures'] = values['module'].lecture_set.all
    values['faqs'] = FAQQuestion.objects.filter(module=values['module'])
    return render(request, 'faqs.html', values)

class CreateFAQQuestionView(CreateView):
    model = FAQQuestion
    form = CreateFAQQuestionForm
    template_name = "faqquestion_form.html"

    def form_valid(self, form):
        faq_question = form.save(commit=False)
        faq_question.author = self.request.user
        faq_question.module = Module.objects.get(pk=self.kwargs['module_id'])
        faq_question.save()
        return super(CreateFAQQuestionView, self).form_valid(form)


class CreateFAQAnswerView(CreateView):
    model = FAQQuestion
    form = CreateFAQAnswerForm
    template_name = "faqanswer_form.html"

    def form_valid(self, form):
        faq_answer = form.save(commit=False)
        faq_answer.author = self.request.user
        faq_question.save()
        return super(CreateFAQAnswerView, self).form_valid(form)