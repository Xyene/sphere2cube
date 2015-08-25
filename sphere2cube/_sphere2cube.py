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
    _args = _parser.parse_args()

    if _args.file_path is None:
        _parser.print_help()
        sys.exit(0)

    face_format = _args.path.replace('%n', '#').replace('%r', str(_args.resolution))

    script = '''
import bpy

bpy.data.textures[0].image = bpy.data.images.load("%s")
bpy.context.scene.render.resolution_x = %d
bpy.context.scene.render.resolution_y = %d
bpy.ops.render.render(animation=True)
    ''' % (_args.file_path, _args.resolution, _args.resolution)

    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as temp:
        temp.write(script)
        temp.flush()

        process = subprocess.Popen(
            ['blender', '--background', '-noaudio', '-b',
             os.path.join(os.path.dirname(os.path.realpath(__file__)), 'cubemapgen.blend'),
             '-o', face_format, '-F', _args.format, '-x', '1', '-P', temp.name]
            + (['-t', _args.threads] if _args.threads else []))

        process.wait()
