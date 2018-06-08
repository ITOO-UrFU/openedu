from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from django.forms import *
from .models import *


class Thanks(TemplateView):
    template_name = 'questionnaire/thanks.html'


class EIOSForm(ModelForm):
    SERVICES = (
        ("0", "Электронные библиотечные сервисы"),
        ("1", "СДО «Гиперметод»"),
        ("2", "СДО «Портал электронного обучения на базе Moodle»"),
        ("3", "Платформа онлайн-обучения «openedu.urfu.ru»"),
        ("4", "Личный кабинет преподавателя"),
        ("5", "Ни одним из этих")
    )
    q2 = MultipleChoiceField(choices=SERVICES, widget=CheckboxSelectMultiple(), label="Какими корпоративными сервисами Уральского федерального университета вы пользуетесь?")

    def clean_q2(self):
        return self.cleaned_data['q2']

    class Meta:
        model = EIOS
        fields = ["q1", "q2", "q3", "q4", "q5", "q6", "q7", "q8", "q9", "q10", "q11", "q12", "q13", "q14", "q15", "q16"]
        widgets = {
            'q1': RadioSelect(),
            'q3': RadioSelect(),
            'q4': RadioSelect(),
            'q5': RadioSelect(),
            'q6': RadioSelect(),
            'q7': RadioSelect(),
            'q8': RadioSelect(),
            'q9': RadioSelect(),
            'q10':Textarea(),
            'q11': RadioSelect(),
            'q12': NumberInput(),
            'q13': RadioSelect(),
            'q14': RadioSelect(),
            'q15': EmailInput(),
        }


class EIOSView(FormView):
    template_name = 'questionnaire/EIOS.html'
    form_class = EIOSForm
    success_url = '/questionnaire/thanks/'

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(EIOSView, self).get_context_data(**kwargs)
        context['qlist'] = ["q3", "q4", "q5", "q6", "q7", "q8", "q9"]
        return context


eios = EIOSView.as_view()
