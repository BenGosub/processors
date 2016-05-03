# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

import sys
import dataset
from importlib import import_module
from . import config


# Module API

def cli(argv):

    # Prepare conf dict
    conf = {}
    for name, value in vars(config).items():
        if name.isupper():
            conf[name] = value

    # Prepare conn dict
    conn = {}
    conn['database'] = dataset.connect(config.DATABASE_URL)
    conn['warehouse'] = dataset.connect(config.WAREHOUSE_URL)

    # Get and call processor
    process = import_module('processors.%s' % argv[1]).process
    process(conf, conn, *argv[2:])


if __name__ == '__main__':
    cli(sys.argv)
