#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using
the function do_deploy
"""

from fabric.api import put, run, env
from os.path import exists
env.hosts = ['54.90.57.18', '35.153.51.85']


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
