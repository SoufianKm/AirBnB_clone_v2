#!/usr/bin/python3
"""
Fabric script (based on the file 2-do_deploy_web_static.py)
that creates and distributes an archive to your web
servers, using the function deploy
"""

from fabric.api import *
from datetime import datetime
from os.path import exists, isdir
env.hosts = ['3.84.255.201', '100.25.151.69']

def do_pack():
    """
    compressed archive file of web_static folder
    """
    ref = 'web_static_' + datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = ref + '.' + 'tgz'
    if isdir("versions") is False:
        local('mkdir -p versions')
    create = local('tar -cvzf versions/{} web_static'.format(file_name))
    if create.succeeded:
        return 'versions/{}'.format(file_name)
    else:
        return None


def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if exists(archive_path) is False:
        return False
    try:
        # essential file names
        file_name = archive_path.split("/")[-1]
        extract_path = file_name.split(".")[0]
        full_path = "/data/web_static/releases/"
        link = "/data/web_static/current"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(full_path, extract_path))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, full_path,
            extract_path))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(full_path, extract_path))
        run('rm -rf {}{}/web_static'.format(full_path, extract_path))
        run('rm -rf {}'.format(link))
        run('ln -s {}{}/ {}'.format(full_path, extract_path, link))
        return True
    except:
        return False


def deploy():
    """creates and distributes an archive to the web servers"""
    archive_path = do_pack()
    if archive_path is None:
        return False
    return do_deploy(archive_path)
