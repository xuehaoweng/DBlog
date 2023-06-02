#!/bin/bash

cd /home/blog_backend
pip3 install --upgrade pip -i https://mirrors.aliyun.com/pypi/simple/
pip3 install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

python3 manage.py collectstatic --noinput

web(){
    mkdir -p /app/logs/celery_logs
    mkdir -p /var/log/supervisor
    rm -rf /app/logs/celery_logs/w*.log
    rm -rf *.pid
    echo 'uwsgi done'
    supervisord -n -c /app/supervisord_prd.conf
}


case "$1" in
web)
web
;;
*)
echo "Usage: $1 {web}"
;;
esac
echo "start running!"