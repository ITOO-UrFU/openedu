import logging
import datetime
import json
from openedu.celery import app
from .models import Course, Platform, Owner, Area, Direction


from time import gmtime, strftime


logger = logging.getLogger('celery_logging')


@app.task(bind=True)
def update_courses_from_roo_task(self, *args):
    # logger.info("Course Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Course.updade_courses_from_roo()


@app.task(bind=True)
def update_platform_from_roo_task(*args):
    # logger.info("Platform Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Platform.get()


@app.task(bind=True)
def update_owner_from_roo_task(*args):
    # logger.info("Owner Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Owner.get()


@app.task(bind=True)
def update_areas_from_roo_task(*args):
    # logger.info("Areas Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Area.get()


@app.task(bind=True)
def update_direction_from_roo_task(*args):
    # logger.info("Direction Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Direction.get()


@app.task(bind=True)
def courses_set_identical_task(*args):
    # logger.info("Areas Начали: {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))
    Course.find_duplicates()

# app.control.rate_limit('roo.tasks,update_courses_from_roo_task', '5/m')
# app.control.rate_limit('roo.tasks,update_platform_from_roo_task', '5/m')
