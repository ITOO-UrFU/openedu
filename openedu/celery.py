import os
from celery import Celery

from django.conf import settings

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'openedu.openedu')

app = Celery('django.conf:settings')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('openedu.celeryconfig')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

app.conf.beat_schedule = {
    # 'add-every-2-seconds': {
    #     'task': 'openprofession.views.handle_report',
    #     'schedule': 2.0,
    #     'args': (1, 1)
    # },
    # 'set_possible_id': {
    #     'task': 'openprofession.views.set_possible_id',
    #     'schedule': 600.0,
    #     'args': (1, 1)
    # },
    # 'set_course_user_grade': {
    #     'task': 'openprofession.views.set_course_user_grade',
    #     'schedule': 600.0,
    #     'args': (1, 1)
    # },
    # 'set_program_grade': {
    #     'task': 'openprofession.views.set_program_grade',
    #     'schedule': 600.0,
    #     'args': (1, 1)
    # },
    # 'set_proctoring_status': {
    #     'task': 'openprofession.views.set_proctoring_status',
    #     'schedule': 600.0,
    #     'args': (1, 1)
    # },

    'update_platform_from_roo_task': {
        'task': 'roo.tasks.update_platform_from_roo_task',
        'args': (1, 1)
    },
    'update_courses_from_roo_task': {
        'task': 'roo.tasks.update_courses_from_roo_task',
        'args': (1, 1)
    }
}


# set_proctoring_status
