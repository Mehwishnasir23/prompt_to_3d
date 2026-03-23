import os
import math
import re


class OBJModel:
    def __init__(self):
        self.vertices = []
        self.objects = []
        self.current_object = None
        self.material_name = "wood_mat"
        self.material_color = (0.6, 0.4, 0.2)

    def set_material(self, name, color_rgb):
        self.material_name = name
        self.material_color = color_rgb

    def start_object(self, name):
        self.current_object = {"name": name, "faces": []}
        self.objects.append(self.current_object)

    def add_cube(self, x, y, z, w, h, d):
        if not self.current_object: self.start_object("part")
        start = len(self.vertices) + 1
        hw, hh, hd = w / 2, h / 2, d / 2
        verts = [(x - hw, y - hh, z - hd), (x + hw, y - hh, z - hd), (x + hw, y + hh, z - hd), (x - hw, y + hh, z - hd),
                 (x - hw, y - hh, z + hd), (x + hw, y - hh, z + hd), (x + hw, y + hh, z + hd), (x - hw, y + hh, z + hd)]
        self.vertices.extend(verts)
        faces = [(start, start + 1, start + 2, start + 3), (start + 4, start + 5, start + 6, start + 7),
                 (start, start + 1, start + 5, start + 4), (start + 2, start + 3, start + 7, start + 6),
                 (start + 1, start + 2, start + 6, start + 5), (start, start + 3, start + 7, start + 4)]
        self.current_object["faces"].extend(faces)

    def add_solid_disc(self, x, y, z, radius, height, segments=32):
        if not self.current_object: self.start_object("disc_part")
        top_start = len(self.vertices) + 1
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            self.vertices.append((x + radius * math.cos(angle), y + height / 2, z + radius * math.sin(angle)))
        bottom_start = len(self.vertices) + 1
        for i in range(segments):
            angle = (2 * math.pi * i) / segments
            self.vertices.append((x + radius * math.cos(angle), y - height / 2, z + radius * math.sin(angle)))
        for i in range(segments):
            v1, v2 = top_start + i, top_start + (i + 1) % segments
            v3, v4 = bottom_start + (i + 1) % segments, bottom_start + i
            self.current_object["faces"].append((v1, v2, v3, v4))
        top_c = len(self.vertices) + 1
        self.vertices.append((x, y + height / 2, z))
        bottom_c = len(self.vertices) + 1
        self.vertices.append((x, y - height / 2, z))
        for i in range(segments):
            self.current_object["faces"].append((top_start + i, top_start + (i + 1) % segments, top_c))
            self.current_object["faces"].append((bottom_start + i, bottom_start + (i + 1) % segments, bottom_c))

    def export(self, filename):
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        mtl_file = filename.replace(".obj", ".mtl")
        with open(mtl_file, "w") as mtl:
            mtl.write(
                f"newmtl {self.material_name}\nKd {self.material_color[0]} {self.material_color[1]} {self.material_color[2]}\n")
        with open(filename, "w") as f:
            f.write(f"mtllib {os.path.basename(mtl_file)}\n")
            for v in self.vertices: f.write(f"v {v[0]:.4f} {v[1]:.4f} {v[2]:.4f}\n")
            for obj in self.objects:
                f.write(f"\no {obj['name']}\nusemtl {self.material_name}\n")
                for face in obj["faces"]: f.write("f " + " ".join(map(str, face)) + "\n")


def generate_furniture(params, output_file="outputs/furniture.obj"):
    model = OBJModel()
    prompt = params.get("raw_prompt", "").lower()

    # --- 1. MATERIAL DETECTION ---
    if "white" in prompt:
        model.set_material("white", (0.9, 0.9, 0.9))
    elif "black" in prompt:
        model.set_material("black", (0.1, 0.1, 0.1))
    elif "walnut" in prompt:
        model.set_material("walnut", (0.27, 0.13, 0.05))
    else:
        model.set_material("oak", (0.6, 0.45, 0.25))

    # --- 2. DYNAMIC LEG COUNT EXTRACTION ---
    leg_match = re.search(r'(\d+)\s*legs', prompt)
    leg_count = int(leg_match.group(1)) if leg_match else 4

    # --- 3. SURFACES (Tables/Desks) ---
    if "table" in prompt or "desk" in prompt:
        model.start_object("table_top")
        if "round" in prompt:
            model.add_solid_disc(0, 75, 0, 55, 4)
        else:
            model.add_cube(0, 75, 0, 110, 4, 110)

        radius_offset = 40 if "round" in prompt else 35
        for i in range(leg_count):
            angle = (2 * math.pi * i) / leg_count
            model.start_object(f"leg_{i + 1}")
            model.add_cube(radius_offset * math.cos(angle), 37.5, radius_offset * math.sin(angle), 4, 75, 4)

    # --- 4. SLEEPING (Beds) ---
    elif "bed" in prompt:
        model.start_object("bed_base")
        model.add_cube(0, 15, 0, 160, 20, 200)
        if "headboard" in prompt:
            model.start_object("headboard")
            model.add_cube(0, 65, -95, 160, 100, 8)
        for i in range(4):
            x, z = (70 if i < 2 else -70), (90 if i % 2 == 0 else -90)
            model.start_object(f"bed_leg_{i + 1}")
            model.add_cube(x, 2.5, z, 10, 5, 10)

    # --- 5. SEATING (Chairs/Stools) ---
    elif "chair" in prompt or "stool" in prompt:
        model.start_object("seat")
        model.add_cube(0, 45, 0, 45, 5, 45)
        for i in range(leg_count):
            angle = (2 * math.pi * i) / leg_count
            model.start_object(f"leg_{i + 1}")
            model.add_cube(18 * math.cos(angle), 22.5, 18 * math.sin(angle), 4, 45, 4)

        if "chair" in prompt and "no backrest" not in prompt:
            model.start_object("backrest")
            model.add_cube(0, 85, -20, 45, 40, 4)

        if "armrest" in prompt:
            for side in [-22, 22]:
                model.start_object(f"armrest_{'l' if side < 0 else 'r'}")
                model.add_cube(side, 65, 0, 4, 2, 40)
                model.add_cube(side, 55, 15, 4, 20, 4)

    # --- 6. STORAGE (Cabinets/Wardrobes) ---
    elif "cabinet" in prompt or "wardrobe" in prompt:
        model.start_object("body")
        model.add_cube(0, 85, 0, 85, 170, 45)
        if "drawers" in prompt:
            for i in range(4):
                model.start_object(f"drawer_{i + 1}")
                model.add_cube(0, 30 + (i * 35), 20, 75, 25, 5)

    model.export(output_file)
    return output_file