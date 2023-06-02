FROM python:3.9.16-slim
RUN sed -i s@/deb.debian.org/@/mirrors.aliyun.com/@g /etc/apt/sources.list
RUN set -ex \
  && apt-get update\
  && apt-get install gcc -y\
  && apt-get install git -y \
  && apt-get install libmysqlclient-dev

COPY . /app

# 再次切换工作目录为Django主目录
WORKDIR /app

# 安装项目所需python第三方库
# 指定setuptools的版本，必须指定，新版本有兼容问题
RUN set -ex \
    && pip install setuptools_scm -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --upgrade pip setuptools==45.2.0 -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && rm -rf /var/cache/yum/*

RUN set -ex \
 && python manage.py collectstatic --noinput \
 && python manage.py makemigrations \
 && python manage.py migrate  --fake

#EXPOSE 8000
EXPOSE 8001
CMD ["sh", "start.sh"]