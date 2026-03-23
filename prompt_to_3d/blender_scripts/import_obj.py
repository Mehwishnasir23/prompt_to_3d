import bpy
import sys
import os

# -----------------------------
# Get OBJ path from arguments
# -----------------------------
argv = sys.argv
argv = argv[argv.index("--") + 1:] if "--" in argv else []

if not argv:
    print("No OBJ path provided")
    quit()

obj_path = argv[0]

if not os.path.exists(obj_path):
    print("OBJ not found:", obj_path)
    quit()

# -----------------------------
# Clear default scene
# -----------------------------
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete()

# -----------------------------
# IMPORT OBJ (Blender 5.0 way)
# -----------------------------
bpy.ops.wm.obj_import(filepath=obj_path)

print("OBJ imported successfully:", obj_path)
