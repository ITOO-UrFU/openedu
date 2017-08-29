from django.shortcuts import render
from django.conf import settings
import requests
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session
import json

client_id = r'9591da81e267b6680b0f'
client_secret = r'ebac4e7063c5483ea3f001b37d73c9c747223a1f'
redirect_uri = 'https://127.0.0.1/courses/'


class Course:
    #  block_url, effort, end, enrollment_start, enrollment_end, id, media, name, number, org,
    #  short_description, start, start_display, start_type, pacing, mobile_available, hidden, course_id
    def __init__(self, **entries):
        self.__dict__.update(entries)

    def __str__(self):
        return self.name


def courses(request):
    LMS_BASE = settings.LMS
    LMS_API_COURSES = f"{LMS_BASE}{settings.LMS_API_COURSES}"
    courses = []

    auth = HTTPBasicAuth(client_id, client_secret)
    client = BackendApplicationClient(client_id=client_id)
    oauth = OAuth2Session(client=client)
    token = oauth.fetch_token(token_url=f'{LMS_BASE}oauth2/access_token/', auth=auth, verify=False)
    access_token = token["access_token"]
    id_token = token["id_token"]
    token_type = token["token_type"]
    headers = {'Authorization': f'{token_type} {access_token}'}

    r = requests.get(LMS_API_COURSES, verify=False)
    pagination = r.json()["pagination"]

    # courses_count = pagination["count"]
    pages_count = pagination["num_pages"]

    for course in r.json()["results"]:
        if course["hidden"] == False:
            courses.append(Course(**course))

    for page in range(2, pages_count + 1):
        r = requests.get(f"{LMS_API_COURSES}?page={page}", verify=False)
        if course["hidden"] == False:
            courses.append(Course(**course))

    msg = []

    for course in courses:
        payload = {
            "course_id": course.id,
            "all_blocks": True,
            "requested_fields": "graded,format,student_view_multi_device,student_view_data,children",
            "username": "openedu",
            "type": "course,chapter,sequential,vertical,html,video,problem",
            "block_counts": "video,html,problem",
            "access_token": access_token,
        }
        r = requests.get(
            f'{LMS_BASE}api/courses/v1/blocks/', params=payload,
            headers=headers, verify=False)
        msg.append((r.json()))

    msg = json.dumps(msg)

    return render(request, "courses/courses.html",
                  {
                      "courses": courses,
                      "LMS_BASE": LMS_BASE,
                      "access_token": access_token,
                      "id_token": id_token,
                      "token_type": token_type,
                      "msg": msg,
                  }
                  )

    # def course(request, id):
