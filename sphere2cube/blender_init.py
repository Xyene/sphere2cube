__author__ = 'Xyene'

import bpy
import sys

bpy.data.textures[0].image = bpy.data.images.load("%s" % sys.argv[-6])
bpy.context.scene.render.resolution_x = bpy.context.scene.render.resolution_y = int(sys.argv[-5])

sphere = bpy.data.objects["Sphere"]
sphere.rotation_mode = 'XYZ'
sphere.rotation_euler = (float(sys.argv[-4]), float(sys.argv[-3]), float(sys.argv[-2]))

bpy.data.cameras['Camera'].angle = float(sys.argv[-1])

bpy.data.meshes["Sphere"].use_auto_texspace = 0
bpy.data.meshes["Sphere"].texspace_size[0] = -1

bpy.ops.render.render(animation=True)
