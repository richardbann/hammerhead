from pathlib import Path
import shutil
# import logging

# log = logging.getLogger('gsrun')


def ensure_dir(path, name, user=0, group=0, mode=0o555):
    path = Path(path).joinpath(name)
    path.mkdir(exist_ok=True)
    shutil.chown(path, user, group)
    path.chmod(mode)
