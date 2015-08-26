# sphere2cube
`sphere2cube` is a Python script to map an equirectangular (cylindrical projection; skysphere) map into 6 cube (cubemap; skybox) faces.

```shell
$> sphere2cube -h
usage: sphere2cube.py [-h] [-r RESOLUTION] [-t THREADS] [-p PATH]
                             [-f FORMAT] [-o OUTPUT_DIR] [-R X Y Z]
                             [file_path]

Maps an equirectangular (cylindrical projection; skysphere) map into 6 cube
(cubemap; skybox) faces.

positional arguments:
  file_path             equirectangular image file path

optional arguments:
  -h, --help            show this help message and exit
  -r RESOLUTION, --resolution RESOLUTION
                        resolution for each cube face generated
  -R X Y Z, --rotation X Y Z
                        rotation in degrees to apply before rendering cube
                        faces, x y z format (z is up)
  -p PATH, --path PATH  pattern to save rendered faces: default is
                        "face_%n_%r", where %n is face number, and %r is
                        resolution
  -o OUTPUT_DIR, --output-dir OUTPUT_DIR
                        output directory for faces
  -f FORMAT, --format FORMAT
                        format to use when saving faces, i.e. "PNG" or "TGA"
  -t THREADS, --threads THREADS
                        number of threads to use when rendering
```

Output formats supported depend on the Blender installation, but will generally be TGA, IRIS, HAMX, FTYPE, JPEG, MOVIE, IRIZ, RAWTGA, AVIRAW, AVIJPEG, PNG, BMP, and FRAMESERVER.

`sphere2cube` can be run in a headless environment.

# Examples
For example, to render a 2048-resolution TGA cubemap from `source.jpg`, we could use:
```
$ sphere2cube source.jpg -r2048 -f TGA
```
which would generate `face_1_2048.tga`, ..., `face_6_2048.tga` in the working directory.

# Installation
`sphere2cube` can be easily installed with `pip`. It depends on Blender being installed on the system.

## Linux

```shell
$ apt-get install blender
$ pip install https://github.com/Xyene/sphere2cube/zipball/master
```

## Windows
Install [Blender](https://www.blender.org/), and add `blender.exe` to `PATH`. Finally,

```shell
pip install https://github.com/Xyene/sphere2cube/zipball/master
```
