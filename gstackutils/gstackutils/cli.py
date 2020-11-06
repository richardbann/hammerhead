import asyncio

import click
from gstackutils.tools import ensure_dir
from gstackutils import gsrun


@click.group()
def cli():
    pass


@cli.command()
def nginx():
    ensure_dir("/app_home", "logs")
    ensure_dir("/app_home/logs", "nginx", user="nginx", group="nginx")
    ret = asyncio.run(
        gsrun.ProcessList(
            gsrun.Process("nginx", "-c", "/src/conf/nginx.conf"),
        ).start()
    )
    sys.exit(ret)
