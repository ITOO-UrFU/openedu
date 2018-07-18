import logging
import datetime
import json

from openedu.celery import app
from .models import Course

logger = logging.getLogger(__name__)


@app.task(bind=True)
def update_courses_from_roo_task(*args):
    login = 'vesloguzov@gmail.com'
    password = 'ye;yj,jkmitrjlf'

    def get_courses_from_page(page_url):
        request = requests.get(page_url, auth=(login, password))
        response = request.json()
        courses = response["rows"]
        for c in courses:
            r = requests.get('https://online.edu.ru/api/courses/v0/course/' + c['global_id'],
                             auth=('vesloguzov@gmail.com', 'ye;yj,jkmitrjlf'))
            course = r.json()
            roo_course = Course.objects.get_or_create(global_id=course['global_id'],
                                                      defaults={'created_at': course['created_at'],
                                                                'finished_at': course['finished_at'],
                                                                'title': course['title']})[0]
            roo_course.save()
        print("response[next]= ", response["next"])
        if response["next"] is not None:
            get_courses_from_page(response["next"])
        else:
            return

    get_courses_from_page('https://online.edu.ru/api/courses/v0/course')


app.control.rate_limit('roo.tasks.update_courses_from_roo_task', '100/m')