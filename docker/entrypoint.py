#!/usr/bin/env python3
import argparse
from utils.utils import ensure_dir, create_secret, read_secret, delete_secret

def nginx(args):
    # create/chown/chmod directories
    ensure_dir("/app_home", "logs")
    ensure_dir("/app_home/logs", "nginx", user="nginx", group="nginx")

    # read certificate files
    store_secret("y", "hello")
    print(read_secret("x"))

    # choose/process config file

    # run the process


def secret_create(args):
    name = args.name
    infile = args.infile
    force = args.force
    create_secret(name, infile.read(), exists_ok=force)


def secret_read(name):
    name = args.name
    print(read_secret(name), end="")


def secret_rm(name):
    name = args.name
    delete_secret(name)

parser = argparse.ArgumentParser()
commands = parser.add_subparsers(required=True, dest="command")

# nginx command
parser_nginx = commands.add_parser("nginx", help="start nginx")
parser_nginx.set_defaults(func=nginx)

# secret command
parser_secret = commands.add_parser("secret", help="manage secrets")
secret_commands = parser_secret.add_subparsers(required=True, dest="subcommand")

parser_secret_create = secret_commands.add_parser("create")
parser_secret_create.add_argument("name", help="the name of the secret")
parser_secret_create.add_argument("infile", help="the file containing the value of the secret (`-` indicates STDIN)", type=argparse.FileType('rb'))
parser_secret_create.add_argument("-f", "--force", action="store_true", help="force overwrite existing secret")
parser_secret_create.set_defaults(func=secret_create)

parser_secret_create = secret_commands.add_parser("read")
parser_secret_create.add_argument("name", help="the name of the secret")
parser_secret_create.set_defaults(func=secret_read)

parser_secret_create = secret_commands.add_parser("rm")
parser_secret_create.add_argument("name", help="the name of the secret")
parser_secret_create.set_defaults(func=secret_rm)


args = parser.parse_args()
args.func(args)
