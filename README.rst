sphere2cube
===========

``sphere2cube`` is a Python script to map an equirectangular
(cylindrical projection; skysphere) map into 6 cube (cubemap; skybox)
faces.

::

    $ sphere2cube -h
    usage: sphere2cube [-h] [-v] [-r <size>] [-R <rx> <ry> <rz>] [-p <pattern>]
                       [-o <dir>] [-f <name>] [-b <path>] [-t <count>] [-V]
                       [<source>]

    Maps an equirectangular (cylindrical projection; skysphere) map into 6 cube
    (cubemap; skybox) faces.

    positional arguments:
      <source>              source equirectangular image file path

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -r <size>, --resolution <size>
                            resolution for each cube face generated
      -R <rx> <ry> <rz>, --rotation <rx> <ry> <rz>
                            rotation in degrees to apply before rendering cube
                            faces, x y z format
      -p <pattern>, --path <pattern>
                            pattern to save rendered faces: default is
                            "face_%n_%r", where %n is face number, and %r is
                            resolution
      -o <dir>, --output-dir <dir>
                            output directory for faces
      -f <name>, --format <name>
                            format to use when saving faces, i.e. "PNG" or "TGA"
      -b <path>, --blender-path <path>
                            path to blender executable (default "blender")
      -t <count>, --threads <count>
                            number of threads to use when rendering (1-64)
      -V, --verbose         enable verbose logging

Output formats supported depend on the Blender installation, but will
generally be TGA, IRIS, JPEG, MOVIE, IRIZ, RAWTGA, AVIRAW, AVIJPEG, PNG,
BMP, and FRAMESERVER.

``sphere2cube`` can be run in a headless environment (for example, a
server).

Examples
========

For example, to render a 2048-resolution TGA cubemap from
``source.jpg``, we could use:

::

    $ sphere2cube source.jpg -r2048 -fTGA

which would generate ``face_1_2048.tga``, …, ``face_6_2048.tga`` in the
working directory.

Installation
============

``sphere2cube`` can be easily installed with ``pip``. It depends on
Blender being installed on the system.

Linux
-----

::

    $ apt-get install blender
    $ pip install https://github.com/Xyene/sphere2cube/zipball/master

Windows
-------

Install `Blender`_, and add ``blender.exe`` to ``PATH``. Finally,

::

    pip install https://github.com/Xyene/sphere2cube/zipball/master

.. _Blender: https://www.blender.org/