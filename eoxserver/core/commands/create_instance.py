#!/usr/bin/env python
#-------------------------------------------------------------------------------
# $Id$
#
# Project: EOxServer <http://eoxserver.org>
# Authors: Fabian Schindler <fabian.schindler@eox.at>
#          Stephan Krause <stephan.krause@eox.at>
#          Stephan Meissl <stephan.meissl@eox.at>
#
#-------------------------------------------------------------------------------
# Copyright (C) 2011 EOX IT Services GmbH
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell 
# copies of the Software, and to permit persons to whom the Software is 
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies of this Software or works derived from this Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#-------------------------------------------------------------------------------

"""
Create a new EOxServer instance. This instance will create a root directory 
with the instance name in the given (optional) directory.
"""

import tempfile
import shutil
import os
import sys
import django.core.management

# tags to be replaced in the template files
TAG_PATH_SRC = "<$PATH_SRC$>"
TAG_PATH_DST = "<$PATH_DST$>"
TAG_INSTANCE_ID = "<$INSTANCE_ID$>"
TAG_MAPSCRIPT = "<$MAPSCRIPT_PATH$>"

def parse_arguments(argv):
    # set up a parser for command line arguments
    description = """Create a new EOxServer instance. This instance 
                  will create a root directory with the instance name in
                  the given (optional) directory.

                  If the --init_spatialite flag is set, then the initial
                  database will be created and initialized.
                  """
    options = [(
            ['-d', '--dir'], {
                'default': '.',
                'help': 'Optional base directory. Defaults to the current directory.'
            }
        ), (
            ['--initial_data'], {
                'metavar': 'DIR',
                'default': False,
                'help': 'Location of the initial data. Must be JSON.'
            }
        ), (
            ['--init_spatialite'], {
                'action': 'store_true',
                'help': 'Flag to initialize the sqlite database.'
            }
        ), (
            ['--mapscript-dir'], {
                'default': False,
                'metavar': 'DIR',
                'help': 'Optional path to the MapServer mapscript library.'
            }
        ), (
            ['instance_id'], {
                'nargs': 1,
                'action': 'store',
                'metavar': 'INSTANCE_ID',
                'help': 'Mandatory name of the eoxserver instance.'
            }
        )
    ]
    
    try:
        # first try with argparse
        import argparse
        parser = argparse.ArgumentParser()
        parser.description = description

        for largs, kwargs in options:
            parser.add_argument(*largs, **kwargs)

        args = parser.parse_args(argv)
        args.instance_id = args.instance_id[0]
        
    except ImportError:
        # Fallback if argparse is not available
        import optparse
        
        parser = optparse.OptionParser()
        parser.description = " ".join([line.strip() for line in description.split("\n")])

        for largs, kwargs in options:
            try:
                parser.add_option(*largs, **kwargs)
            except optparse.OptionError: pass

        parser.usage = "Usage: %s [options] INSTANCE_ID" % sys.argv[0]
        parser.epilog = "  INSTANCE_ID          Mandatory name of the eoxserver instance."
        
        args, positional_args = parser.parse_args(argv)
        
        if len(positional_args) != 1:
            parser.error("Exactly one instance name is expected.")

        args.instance_id = positional_args[0]

    return args

def copy_and_replace_tags(src_pth, dst_pth, replacements={}):
    """Helper function to copy a file and replace tags within a file."""
    new_file = open(dst_pth,'w')
    old_file = open(src_pth)
    for line in old_file:
        for pattern, subst in replacements.iteritems():
            line = line.replace(pattern, subst)
        new_file.write(line)
    new_file.close()
    old_file.close()

def create_file(dir_or_path, file=None):
    """Helper function to create a new empty file at a given location."""
    if file is not None:
        dir_or_path = os.path.join(dir_or_path, file)
    f = open(dir_or_path, 'w')
    f.close()

def execute(argv):
    # parse command line arguments
    args = parse_arguments(argv)

    instance_id = args.instance_id
    
    dst_root_dir = os.path.abspath(args.dir)
    dst_inst_dir = os.path.join(dst_root_dir, instance_id)
    dst_conf_dir = os.path.join(dst_inst_dir, "conf")
    dst_data_dir = os.path.join(dst_inst_dir, "data")
    dst_logs_dir = os.path.join(dst_inst_dir, "logs")
    dst_fixtures_dir = os.path.join(dst_data_dir, "fixtures")

    src_root_dir = os.path.dirname(os.path.abspath(__file__))
    src_conf_dir = os.path.join(src_root_dir, "conf")

    if args.initial_data:
        initial_data = os.path.abspath(args.initial_data)

    os.chdir(dst_root_dir)

    # create the initial django folder structure
    print("Initializing django project folder.")
    django.core.management.call_command("startproject", instance_id)

    # create the `conf`, `data`, `logs` and `fixtures` subdirectories
    os.mkdir(dst_conf_dir)
    os.mkdir(dst_data_dir)
    os.mkdir(dst_logs_dir)
    os.mkdir(dst_fixtures_dir)

    # create an empty logfile
    create_file(dst_logs_dir, "eoxserver.log")
    
    tags = {
        TAG_PATH_SRC: src_root_dir,
        TAG_PATH_DST: dst_inst_dir,
        TAG_INSTANCE_ID: instance_id
    }

    if args.mapscript_dir:
        tags[TAG_MAPSCRIPT] = args.mapscript_dir

    # copy the template settings file and replace its tags
    copy_and_replace_tags(os.path.join(src_conf_dir, "TEMPLATE_settings.py"),
                          os.path.join(dst_inst_dir, "settings.py"),
                          tags)

    # copy the template config file and replace its tags
    copy_and_replace_tags(os.path.join(src_conf_dir, "TEMPLATE_eoxserver.conf"),
                          os.path.join(dst_conf_dir, "eoxserver.conf"),
                          tags)

    shutil.copy(os.path.join(src_conf_dir, "TEMPLATE_template.map"),
                os.path.join(dst_conf_dir, "template.map"))

    if args.initial_data:
        if os.path.splitext(args.initial_data)[1].lower() != ".json":
            raise Exception("Initial data must be a JSON file.")
        shutil.copy(initial_data, os.path.join(dst_fixtures_dir,
                                               "initial_data.json"))
    
    if args.init_spatialite:
        # initialize the spatialite database file
        os.chdir(dst_data_dir)
        db_name = "conf.sqlite"
        print("Setting up initial database.")
        try:
            from pyspatialite import dbapi2 as db
            conn = db.connect(db_name)
            conn.execute("SELECT InitSpatialMetadata()")
            conn.commit()
            conn.close()
        except ImportError:
            init_sql_path = os.path.join(src_conf_dir, "init_spatialite-2.3.sql")
            os.system("spatialite conf.sqlite < %s" % init_sql_path)

if __name__ == "__main__":
    execute(sys.argv[1:])