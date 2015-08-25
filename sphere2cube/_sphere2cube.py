#!/usr/bin/env python
import math

__author__ = 'Tudor'

import argparse
import os
import sys
import tempfile
import subprocess


def main():
    _parser = argparse.ArgumentParser(description='''
        Maps an equirectangular (cylindrical projection; skysphere) map into 6 cube (cubemap; skybox) faces.
    ''')
    _parser.add_argument('file_path', nargs='?',
                         help='equirectangular image file path')
    _parser.add_argument('-r', '--resolution', type=int, default=1024,
                         help='resolution for each cube face generated')
    _parser.add_argument('-t', '--threads', type=int, default=None,
                         help='number of threads to use when rendering')
    _parser.add_argument('-p', '--path', type=str, default='face_%n_%r',
                         help='pattern to save rendered faces: default is '
                              '"face_%%n_%%r", where %%n is face number, and %%r is resolution')
    _parser.add_argument('-f', '--format', type=str, default='TGA',
                         help='format to use when saving faces, i.e. "PNG" or "TGA"')
    _parser.add_argument('-o', '--output-dir', type=str, default=None,
                         help='output directory for faces')
    _parser.add_argument('-R', '--rotation', type=int, nargs=3, default=[0, 0, 0], metavar=('x', 'y', 'z'),
                         help="rotation in degrees to apply before rendering cube faces, x y z format")
    _args = _parser.parse_args()

    rotations = map(lambda x: math.radians(x), _args.rotation)

    if _args.file_path is None:
        _parser.print_help()
        sys.exit(0)

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
        output = os.path.join(output, face_format) if os.path.isabs(output) else os.path.join(os.getcwd(), output, face_format)
    else:
        output = face_format

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp:
        temp.write(script)
        temp.flush()

        process = subprocess.Popen(
            ['blender', '--background', '-noaudio', '-b',
             os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cubemapgen.blend'),
             '-o', output, '-F', _args.format, '-x', '1', '-P', temp.name]
            + (['-t', _args.threads] if _args.threads else []))

        process.wait()
