task_routes = {
    'tasks.add': 'low-priority',
}
task_annotations = {
    'tasks.add': {'rate_limit': '100/m'}
}
task_serializer = 'json'
accept_content = ['json']
result_serializer = 'json'

REDIS_HOST = 'localhost'
REDIS_PORT = '6379'
broker_url = 'redis://' + REDIS_HOST + ':' + REDIS_PORT + '/0'
broker_transport_options = {'visibility_timeout': 3600}
result_backend = 'django-db'
result_expires = 36
