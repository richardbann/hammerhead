#!/usr/bin/env bash
set -e

SOCKET_GID=$(stat -c '%g' /var/run/docker.sock)
if [ "$(cat /etc/group | grep :"${SOCKET_GID}":)" = "" ]; then
    groupadd --gid "${SOCKET_GID}" docker
fi
usermod -aG "${SOCKET_GID}" developer

set +e
exec "$@"
