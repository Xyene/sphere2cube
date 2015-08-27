import bpy
import sys

bpy.data.textures[0].image = bpy.data.images.load("%s" % sys.argv[-5])
bpy.context.scene.render.resolution_x = int(sys.argv[-4])
bpy.context.scene.render.resolution_y = int(sys.argv[-4])

sphere = bpy.data.objects["Sphere"]
sphere.rotation_mode = 'XYZ'
sphere.rotation_euler = (float(sys.argv[-3]), float(sys.argv[-2]), float(sys.argv[-1]))

bpy.ops.render.render(animation=True)