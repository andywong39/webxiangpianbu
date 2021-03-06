#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  WebXiangpianbu Copyright (C) 2013, 2014, 2015 Wojciech Polak
#
#  This program is free software; you can redistribute it and/or modify it
#  under the terms of the GNU General Public License as published by the
#  Free Software Foundation; either version 3 of the License, or (at your
#  option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License along
#  with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import glob
import getopt
import yaml
from django.utils.six.moves import input

try:
    import simplejson as json
except ImportError:
    import json


def main():
    opts = {
        'overwrite': False,
        'output_dir': '',
        'output_name': '',
    }

    try:
        gopts, args = getopt.getopt(sys.argv[1:], 'y',
                                    ['overwrite=',
                                     ])
        for o, arg in gopts:
            if o in ('-y', '--overwrite'):
                opts['overwrite'] = True

        if len(args):
            opts['input'] = glob.glob(args[0])
        else:
            raise getopt.GetoptError('')
        if len(args) > 1:
            opts['output_dir'] = os.path.dirname(args[1])
            opts['output_name'] = os.path.basename(args[1])
    except getopt.GetoptError:
        print("Usage: %s [OPTION...] INPUT OUTPUT" % sys.argv[0])
        print("%s -- album converter" % sys.argv[0])
        print("""
 Options               Default values
 -y, --overwrite       [False]
""")
        sys.exit(1)

    if opts['output_dir'] and not os.path.exists(opts['output_dir']):
        os.makedirs(opts['output_dir'])

    for name in opts['input']:
        data = read_albumfile(name)
        if data:
            if name.endswith('.json'):
                to_yaml(opts, name, data)
            elif name.endswith('.yaml'):
                to_json(opts, name, data)
    print('done')


def read_albumfile(name):
    if os.path.isfile(name) and name.endswith('.yaml'):
        try:
            album_content = open(name, 'r').read()
            return yaml.load(album_content)
        except Exception as e:
            print(e)
    elif os.path.isfile(name) and name.endswith('.json'):
        try:
            album_content = open(name, 'r').read()
            return json.loads(album_content)
        except Exception as e:
            print(e)
    return None


def to_yaml(opts, name, data):
    filename = os.path.join(opts['output_dir'] or os.path.dirname(name),
                            opts['output_name'] or os.path.basename(
                            name.replace('.json', '.yaml')))
    overwrite = True
    if os.path.exists(filename):
        overwrite = opts['overwrite'] or \
            confirm('Overwrite album file %s?' % filename)
    if overwrite:
        with open(filename, 'w') as album_file_yaml:
            yaml.dump(data, album_file_yaml, encoding='utf-8',
                      default_flow_style=False, indent=4, width=70)
            print('saved %s' % album_file_yaml.name)


def to_json(opts, name, data):
    filename = os.path.join(opts['output_dir'] or os.path.dirname(name),
                            opts['output_name'] or os.path.basename(
                            name.replace('.yaml', '.json')))
    overwrite = True
    if os.path.exists(filename):
        overwrite = opts['overwrite'] or \
            confirm('Overwrite album file %s?' % filename)
    if overwrite:
        with open(filename, 'w') as album_file_json:
            json.dump(data, album_file_json, indent=4)
            album_file_json.write('\n')
            print('saved %s' % album_file_json.name)


def confirm(question, default=False):
    if default:
        defval = 'Y/n'
    else:
        defval = 'y/N'
    while True:
        res = input("%s [%s] " % (question, defval)).lower()
        if not res:
            return default
        elif res in ('y', 'yes'):
            return True
        elif res in ('n', 'no'):
            return False


if __name__ == '__main__':
    main()
