FROM ubuntu:focal-20200729

RUN apt-get update && apt-get upgrade -y

RUN apt-get install -y locales
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
 
RUN addgroup --system --gid 101 nginx \
    && adduser --system --disabled-login --ingroup nginx --no-create-home \
               --home /nonexistent --shell /bin/false --uid 101 nginx

RUN apt-get install --no-install-recommends --no-install-suggests -y nginx
RUN apt-get install --no-install-recommends --no-install-suggests -y python3 python3-pip
