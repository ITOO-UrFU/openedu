/usr/local/itoo/envs/openedu/bin/celery -A openedu beat  &
/usr/local/itoo/envs/openedu/bin/celery -A openedu worker --loglevel=INFO --concurrency=10 -n worker1@%h &
/usr/local/itoo/envs/openedu/bin/celery -A openedu worker --loglevel=INFO --concurrency=10 -n worker2@%h &
#/usr/local/itoo/envs/openedu/bin/celery -A openedu worker --loglevel=INFO --concurrency=10 -n worker3@%h &
#/usr/local/itoo/envs/openedu/bin/celery -A openedu worker --loglevel=INFO --concurrency=10 -n worker4@%h &
