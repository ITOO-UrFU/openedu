"""
gunicorn configuration file: http://docs.gunicorn.org/en/develop/configure.html

This file is created and updated by ansible, edit at your peril
"""
import multiprocessing

preload_app = False
timeout = 300
bind = "0.0.0.0:8080"
pythonpath = "/usr/local/itoo/app/openedu"

errorlog = "/usr/local/itoo/var/log/openedu/error.log"
loglevel = 'debug'
accesslog = "/usr/local/itoo/var/log/openedu/access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

workers = 4  # (multiprocessing.cpu_count()-1) * 4 + 4


