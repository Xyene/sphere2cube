#!/usr/bin/env python
import math

__author__ = 'Tudor'
__version__ = '0.1.0'

import argparse
import os
import sys
import tempfile
import subprocess


def main():
    _parser = argparse.ArgumentParser(prog='sphere2cube', description='''
        Maps an equirectangular (cylindrical projection; skysphere) map into 6 cube (cubemap; skybox) faces.
    ''')
    # usage='''
    # In order to create 2048-sized cube faces in TGA format from a map 'source.jpg' and place the resulting images in (a pre-existing) folder 'faces':
    # $ sphere2cube source.jpg -r2048 -fTGA -ofaces
    #     '''
    _parser.add_argument('file_path', nargs='?', metavar='<source>',
                         help='source equirectangular image file path')
    _parser.add_argument('-v', '--version', action='version', version=__version__)
    _parser.add_argument('-r', '--resolution', type=int, default=1024, metavar='<size>',
                         help='resolution for each cube face generated')
    _parser.add_argument('-R', '--rotation', type=int, nargs=3, default=[0, 0, 0], metavar=('<rx>', '<ry>', '<rz>'),
                         help="rotation in degrees to apply before rendering cube faces, x y z format")
    _parser.add_argument('-p', '--path', type=str, default='face_%n_%r', metavar='<pattern>',
                         help='pattern to save rendered faces: default is '
                              '"face_%%n_%%r", where %%n is face number, and %%r is resolution')
    _parser.add_argument('-o', '--output-dir', type=str, default=None, metavar='<dir>',
                         help='output directory for faces')
    _parser.add_argument('-f', '--format', type=str, default='TGA', metavar='<name>',
                         help='format to use when saving faces, i.e. "PNG" or "TGA"')
    _parser.add_argument('-t', '--threads', type=int, default=None, metavar='<count>',
                         help='number of threads to use when rendering (1-64)')
    _parser.add_argument('-V', '--verbose', action='store_true',
                         help='enable verbose logging')
    _args = _parser.parse_args()

    rotations = map(lambda x: math.radians(x), _args.rotation)

    if _args.threads and _args.threads not in range(1, 65):
        _parser.print_usage()
        print('sphere2cube: error: too many threads specified (range is 1-64)')
        sys.exit(1)

    if _args.file_path is None:
        _parser.print_help()
        sys.exit(1)

    face_format = _args.path.replace('%n', '#').replace('%r', str(_args.resolution))

    script = '''
import bpy

bpy.data.textures[0].image = bpy.data.images.load("%s")
bpy.context.scene.render.resolution_x = %d
bpy.context.scene.render.resolution_y = %d

sphere = bpy.data.objects["Sphere"]
sphere.rotation_mode = 'XYZ'
sphere.rotation_euler = (%f, %f, %f)

bpy.ops.render.render(animation=True)
    ''' % (_args.file_path, _args.resolution, _args.resolution, rotations[0], rotations[1], rotations[2])

    output = _args.output_dir
    if output:
        output = output if os.path.isabs(output) else os.path.join(os.getcwd(), output)
        if not os.path.exists(output):
            print("%s does not exist or is not a valid directory" % output)
            sys.exit(1)
        output = os.path.join(output, face_format)
    else:
        output = face_format

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp:
        temp.write(script)
        temp.flush()

        out = open(os.devnull, 'w') if not _args.verbose else None

        process = subprocess.Popen(
            ['blender', '--background', '-noaudio', '-b',
             os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cubemapgen.blend'),
             '-o', output, '-F', _args.format, '-x', '1', '-P', temp.name]
            + (['-t', str(_args.threads)] if _args.threads else []),
            stderr=out, stdout=out)

        process.wait()
