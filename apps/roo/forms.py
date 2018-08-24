from django import forms
from .models import Course

class CourseTableForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = '__all__'

        def __init__(self, *args, **kwargs):
            super(CourseTableForm, self).__init__(*args, **kwargs)