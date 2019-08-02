#!/usr/bin/env python

import argparse
import os
import helmrelease
import sys

from pprint import pprint

class FileIndexer(object):
    dir_suffix = '/application/releases'

    def __init__(self, search_paths):
        self.search_paths = search_paths

    def found(self):
        found = []
        for path in self.search_paths:
            path = path.rstrip(os.sep)
            if os.path.isdir(path):
                for root, dirs, files in os.walk(path):
                    if not root.endswith(self.dir_suffix):
                        continue
                    for f in files:
                        if f.endswith('.yaml'):
                            found.append(os.path.join(root,f))
            elif os.path.isfile(path):
                if not path.endswith(self.dir_suffix):
                    found.append(path)
            else:
                raise FileNotFoundError("A path {} must be either an existing file or directory.".format(path))

        return found

class StoreKeyValue(argparse.Action):
    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        self._nargs = nargs
        super(StoreKeyValue, self).__init__(option_strings, dest, nargs=nargs, **kwargs)

    def __call__(self, parser, namespace, values, option_string=None):
        retval = []
        for value in values:
            try:
                k,v = value.split(':')
            except ValueError:
                raise ValueError('Option {} {} must be specified in key:value format'.format(self.option_strings[0], value))

            parsed = dict(key=k, value=v)
            retval.append(parsed)
            setattr(namespace, self.dest, retval)

def args_spec():
    parser = argparse.ArgumentParser(description='HelmRelease mass-updater tool.',
        formatter_class=argparse.RawDescriptionHelpFormatter)

    parser.add_argument('path', nargs='+', help='path to HelmRelease file(s) or directories')
    parser.add_argument('--dump', action='store_true', help='dump file output to stdout')
    parser.add_argument('--dry-run', action='store_true', help='do not write to the file')
    parser.add_argument('--silent', action='store_true', help='silent mode, don\'t print anything')

    mod = parser.add_argument_group('content modifiers')

    mod.add_argument('--set', '-s',
                         action=StoreKeyValue,
                         nargs='+',
                         metavar='path.to.key:value',
                         help='set or add value')

    mod.add_argument('--set-name', metavar='NAME', help='update metadata.name key')
    mod.add_argument('--set-namespace', metavar='NAME', help='update metadata.namespace key')
    mod.add_argument('--set-image-tag', metavar='TAG', help='update spec.values.image.tag key')

    mod.add_argument('--unset', '-u',
                         nargs='+',
                         metavar='path.to.key',
                         help='delete an existing key')

    return parser.parse_args()

def main():
    try:
        args = args_spec()
        index = FileIndexer(args.path)
        found = index.found()
    except (FileNotFoundError, ValueError) as e:
        sys.exit('Error: %s' % e)

    fs = '.'

    for path in found:
        try:
            hr = helmrelease.load(path)
        except Exception as e:
            sys.exit("Error:\n%s" % e)

        if args.set_name:
            hr.name= args.set_name

        if args.set_namespace:
            hr.namespace= args.set_namespace

        if args.set_image_tag:
            hr.image_tag = args.set_image_tag

        if args.set:
            for item in args.set:
                key = item.get('key')
                value = item.get('value')
                try:
                    hr.get(key, fs)
                    hr.set(key, value, fs)
                except KeyError:
                    hr.add(key, value, fs)

        if args.unset:
            for key in args.unset:
                hr.delete(key, fs)

        if args.dump:
            print('---')
            print('# path: {}'.format(hr.path))
            hr.dump()
        elif args.silent:
            pass
        else:
            print(hr.path)

        if not args.dry_run:
            hr.write()

if __name__== "__main__" :
    main()
