#!/usr/bin/env python

__author__ = 'Xyene'

import argparse
import os
import sys
import subprocess
import math
from .version import __version__


def main():
    _parser = argparse.ArgumentParser(prog='sphere2cube', description='''
        Maps an equirectangular (cylindrical projection; skysphere) map into 6 cube (cubemap; skybox) faces.
    ''')
    _parser.add_argument('file_path', nargs='?', metavar='<source>',
                         help='source equirectangular image file path')
    _parser.add_argument('-v', '--version', action='version', version=__version__)
    _parser.add_argument('-r', '--resolution', type=int, default=1024, metavar='<size>',
                         help='resolution for each cube face generated')
    _parser.add_argument('-R', '--rotation', type=int, nargs=3, default=[0, 0, 0], metavar=('<rx>', '<ry>', '<rz>'),
                         help="rotation in degrees to apply before rendering cube faces, x y z format")
    _parser.add_argument('-F', '--fov', type=int, default=90, metavar=('<angle>'),
                         help="field of view of camera used for rendering cube faces")
    _parser.add_argument('-p', '--path', type=str, default='face_%n_%r', metavar='<pattern>',
                         help='pattern to save rendered faces: default is '
                              '"face_%%n_%%r", where %%n is face number, and %%r is resolution')
    _parser.add_argument('-o', '--output-dir', type=str, default=None, metavar='<dir>',
                         help='output directory for faces')
    _parser.add_argument('-f', '--format', type=str, default='TGA', metavar='<name>',
                         help='format to use when saving faces, i.e. "PNG" or "TGA"')
    _parser.add_argument('-b', '--blender-path', type=str, default='blender', metavar='<path>',
                         help='path to blender executable (default "blender")')
    _parser.add_argument('-t', '--threads', type=int, default=None, metavar='<count>',
                         help='number of threads to use when rendering (1-64)')
    _parser.add_argument('-V', '--verbose', action='store_true',
                         help='enable verbose logging')
    _args = _parser.parse_args()

    rotations = [math.radians(x) for x in _args.rotation]

    if _args.threads and _args.threads not in list(range(1, 65)):
        _parser.print_usage()
        print('sphere2cube: error: too many threads specified (range is 1-64)')
        sys.exit(1)

    if _args.file_path is None:
        _parser.print_help()
        sys.exit(1)

    face_format = _args.path.replace('%n', '#').replace('%r', str(_args.resolution))

    output = _args.output_dir
    if output:
        output = output if os.path.isabs(output) else os.path.join(os.getcwd(), output)
        if not os.path.exists(output):
            print("%s does not exist or is not a valid directory" % output)
            sys.exit(1)
        output = os.path.join(output, face_format)
    else:
        output = os.path.join(os.getcwd(), face_format)

    file_path = _args.file_path if os.path.isabs(_args.file_path) else os.path.join(os.getcwd(), _args.file_path)

    out = open(os.devnull, 'w') if not _args.verbose else None

    cam_fov = math.radians(float(_args.fov))

    try:
        process = subprocess.Popen(
            [_args.blender_path, '--background', '-noaudio',
             # https://aerotwist.com/tutorials/create-your-own-environment-maps/, CC0
             '-b', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'projector.blend'),
             '-o', output, '-F', _args.format, '-x', '1',
             '-P', os.path.join(os.path.dirname(os.path.realpath(__file__)), 'blender_init.py')]
            + (['-t', str(_args.threads)] if _args.threads else [])
            + ['--', file_path, str(_args.resolution), str(rotations[0]), str(rotations[1]), str(rotations[2]),
               str(cam_fov)],
            stderr=subprocess.PIPE, stdout=out)

        _, stderr = process.communicate()

        if stderr:
            print('error invoking blender:\n %s' % stderr)

        if process.returncode:
            print('blender exited with error code %d' % process.returncode)
            sys.exit(process.returncode)
    except:
        print('error spawning blender (%s) executable' % _args.blender_path)
        import traceback

        traceback.print_exc()
        sys.exit(1)
