#!/usr/bin/python3
"""
Fabric script (based on the file 1-pack_web_static.py)
that distributes an archive to your web servers, using
the function do_deploy:
    Returns False if the file at the path archive_path doesn’t exist
    The script should take the following steps:
        Upload the archive to the /tmp/ directory of the web server.
        Uncompress the archive to the folder
        /data/web_static/releases/<archive filename
        without extension> on the web server.
        Delete the archive from the web server.
        Delete the symbolic link /data/web_static/current
        from the web server.
        Create a new the symbolic link /data/web_static/current
        on the web server, linked to the new version of your code
        (/data/web_static/releases/<archive filename without extension>).
        All remote commands must be executed on your both web servers
        (using env.hosts = ['<IP web-01>', 'IP web-02'] variable in
        your script).
        Returns True if all operations have been done correctly
        otherwise returns False.
        You must use this script to deploy it on your
        servers: xx-web-01 and xx-web-02.
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
        extract_folder = file_name.split(".")[0]
        full_path = "/data/web_static/releases/"
        link = "/data/web_static/current"
        put(archive_path, '/tmp/')
        run('mkdir -p {}{}/'.format(full_path, extract_folder))
        run('tar -xzf /tmp/{} -C {}{}/'.format(file_name, full_path,
            extract_folder))
        run('rm /tmp/{}'.format(file_name))
        run('mv {0}{1}/web_static/* {0}{1}/'.format(full_path, extract_path))
        run('rm -rf {}{}/web_static'.format(full_path, extract_path))
        run('rm -rf {}'.format(link))
        run('ln -s {}{}/ {}'.format(full_path, extract_path, link))
        return True
    except:
        return False
