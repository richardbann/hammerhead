FROM ubuntu:latest

RUN apt-get update && apt-get install -y locales
RUN localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8
ENV TZ=UTC
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

RUN apt-get update && apt-get install -y git make

# python
RUN apt-get update && apt-get install -y python3 python3-venv python3-dev
ENV PYTHONUNBUFFERED 1
ENV PYTHONPYCACHEPREFIX /tmp/__pycache__

RUN groupadd developer --gid=2000 && useradd -m -g developer --uid=2000 developer

COPY entrypoint.sh /usr/local/share/entrypoint.sh
RUN chown developer:root /usr/local/share/entrypoint.sh
ENTRYPOINT ["/usr/local/share/entrypoint.sh"]
CMD [ "sleep", "infinity" ]

RUN apt-get update && apt-get install -y \
      apt-transport-https \
      ca-certificates \
      curl \
      gnupg-agent \
      software-properties-common \
    && curl -fsSL https://download.docker.com/linux/ubuntu/gpg | apt-key add - \
    && add-apt-repository \
       "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
       $(lsb_release -cs) \
       stable" \
    && apt-get update && apt-get install -y docker-ce-cli
