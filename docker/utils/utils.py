from pathlib import Path
import shutil
import base64
import logging

log = logging.getLogger('gsrun')


def ensure_dir(path, name, user=0, group=0, mode=0o555):
    path = Path(path).joinpath(name)
    path.mkdir(exist_ok=True)
    shutil.chown(path, user, group)
    path.chmod(mode)


def read_secrets():
    ret = {}
    with open("/app_home/.secret.env", "r") as f:
        for line in f.readlines():
            line = line.strip()
            p = line.find("=")
            ret[line[:p]] = line[p + 1:]
    return ret


def write_secrets(secrets):
    with open("/app_home/.secret.env", "w") as f:
        for name, value in secrets.items():
            f.write(f"{name}={value}\n")


def read_secret(name, default=None, is_string=True):
    secrets = read_secrets()
    ret = base64.b64decode(secrets[name])
    if is_string:
        return ret.decode()
    return ret


def create_secret(name, value, exists_ok=False):
    secrets = read_secrets()
    if name in secrets and not exists_ok:
        raise KeyError(f"Secret already exists: {name}")
    if isinstance(value, str):
        value = value.encode()
    secrets[name] = base64.b64encode(value).decode()
    write_secrets(secrets)


def delete_secret(name):
    secrets = read_secrets()
    del secrets[name]
    write_secrets(secrets)


def provide_secret(name, default, user=0, group=0, mode=0o400):
    """Should be used by entrypoint"""

    if Path("/run/secrets").joinpath(name).isfile():
        log.info(f"Secret [{name}] exists")
        return
    with open(f"/run/secrets/{name}", "wb") as f:
        f.write(read_secret(name, default))
    shutil.chown(f"/run/secrets/{name}", user, group)
    path.chmod(mode)


def get_secret(name):
    """Should be used by application code"""
    pass
