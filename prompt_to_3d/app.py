from flask import Flask, render_template, request, jsonify, send_from_directory
from nlp.prompt_parser import parse_prompt
from nlp.component_reasoner import infer_components
from generator.furniture_generator import generate_furniture
from editor.furniture_editor import apply_edit
import os
import subprocess

app = Flask(__name__)

# Static folder configuration
STATIC_OUTPUT_DIR = os.path.join('static', 'outputs')
OUTPUT_PATH = os.path.join(STATIC_OUTPUT_DIR, "furniture.obj")

# Blender Path
BLENDER_PATH = r"C:\Program Files\Blender Foundation\Blender 5.0\blender.exe"

def open_in_blender(obj_path):
    abs_obj = os.path.abspath(obj_path)
    script_path = os.path.abspath("blender_scripts/import_obj.py")
    if os.path.exists(BLENDER_PATH):
        subprocess.Popen([BLENDER_PATH, "--python", script_path, "--", abs_obj])
    else:
        print(f"Warning: Blender not found at {BLENDER_PATH}")

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json() # JSON data fetch karein
    user_prompt = data.get("prompt")
    edit = data.get("edit", "")

    if not user_prompt:
        return jsonify({"success": False, "error": "No prompt provided"}), 400

    # 1️⃣ NLP & Reasoning - Prompt ko 'raw_prompt' key mein dena zaroori hai
    params = {"raw_prompt": user_prompt}
    params.update(parse_prompt(user_prompt))
    params = infer_components(params)

    # 2️⃣ Editing
    if edit:
        params = apply_edit(params, edit)

    # 3️⃣ Procedural Generation
    try:
        # Static folder mein save karein taake Three.js access kar sake
        generate_furniture(params, OUTPUT_PATH)
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

    # 4️⃣ Blender Auto-Open (Background mein chalega)
    open_in_blender(OUTPUT_PATH)

    # 5️⃣ Web friendly path return karein
    web_path = "/" + OUTPUT_PATH.replace(os.sep, '/')
    return jsonify({
        "success": True,
        "file_path": web_path
    })

@app.route('/download')
def download_file():

    return send_from_directory(STATIC_OUTPUT_DIR, "furniture.obj", as_attachment=True)

if __name__ == "__main__":
    os.makedirs(STATIC_OUTPUT_DIR, exist_ok=True)
    app.run(debug=True)