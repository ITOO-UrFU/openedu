from django.views.generic.edit import CreateView, BaseCreateView
from .models import File


class FileCreate(CreateView):
    model = File
    success_url = "addfile"
    fields = ['file']

    def get_context_data(self, **kwargs):
        ctx = super(FileCreate, self).get_context_data(**kwargs)
        ctx['files'] = File.objects.all()

        return ctx
