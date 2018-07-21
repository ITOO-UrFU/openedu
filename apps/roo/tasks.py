import logging
import datetime
import json
from openedu.celery import app
from .models import Course

logger = logging.getLogger('celery_logging')


@app.task(bind=True)
def update_courses_from_roo_task(*args):
    logger.info("RUN TASKS!!!!!")
    Course.updade_courses_from_roo()


app.control.rate_limit('roo.tasks.update_courses_from_roo_task', '5/m')
