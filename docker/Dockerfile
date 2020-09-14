FROM ubuntu:focal-20200729

RUN apt-get update && apt-get install -y locales
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN apt-get update && apt-get install -y wget gnupg2

# python
RUN apt-get update && apt-get install -y python3 python3-venv python3-dev
RUN python3 -m venv /python
ENV PATH /python/bin:$PATH
ENV PYTHONUNBUFFERED 1
ENV PYTHONPYCACHEPREFIX /__pycache__

# nginx
RUN groupadd -r nginx --gid=4430 && useradd -r -g nginx --uid=4430 nginx
RUN wget http://nginx.org/keys/nginx_signing.key
RUN apt-key add nginx_signing.key
RUN sh -c "echo 'deb http://nginx.org/packages/mainline/ubuntu/ focal nginx' > /etc/apt/sources.list.d/nginx.list"
RUN apt-get update && apt-get install -y nginx

# RUN pip install --no-cache-dir bullet
COPY / /app_home

ENTRYPOINT ["/app_home/docker/entrypoint.py"]
