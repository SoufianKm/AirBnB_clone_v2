#!/usr/bin/python3
"""
Fabric script that generates a .tgz archive
from the contents of the web_static folder
of AirBnB Clone repo, using the function do_pack
"""

from datetime import datetime
from fabric.api import *


def do_pack():
    """
    compressed archive file of web_static folder
    """
    ref = 'web_static_' + datetime.now().strftime("%Y%m%d%H%M%S")
    file_name = ref + '.' + 'tgz'
    local('mkdir -p versions')
    create = local('tar -czvf versions/{} web_static'.format(file_name))
    if create.succeeded:
        return 'versions/{}'.format(file_name)
    else:
        return None
