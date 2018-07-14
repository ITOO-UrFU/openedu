import logging
import datetime
import json
from openedu.celery import app
from .models import Course

logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_courses_from_roo_task(*args):
    Course.updade_courses_from_roo()
    pass


app.control.rate_limit('roo.views.update_courses_from_roo_task', '100/m')