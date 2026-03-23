import re
import json
import os


def load_modular_dataset():
    base_path = "furniture_dataset_final/base_dataset"
    master_data = {}
    if os.path.exists(base_path):
        for filename in os.listdir(base_path):
            if filename.endswith(".json"):
                with open(os.path.join(base_path, filename), "r") as f:
                    # Modular loading of all categories
                    master_data.update(json.load(f))
    return master_data


MASTER_KNOWLEDGE = load_modular_dataset()


def infer_components(params: dict) -> dict:
    prompt = params.get("raw_prompt", "").lower()
    furniture = params.get("furniture_type", "chair").lower()

    # --- Deep Scan from JSON Dataset ---
    # Hum dhundte hain ke prompt mein hamare JSON ki kaunsi values hain
    build_config = {
        "type": furniture,
        "attributes": {},
        "micro_details": {},
        "materials": {}
    }

    # Extract Quantity (e.g., 3 legs, 2 drawers)
    quantities = re.findall(r"(\d+)\s+([a-zA-Z]+)", prompt)
    for qty, item in quantities:
        build_config["attributes"][f"{item.rstrip('s')}_count"] = int(qty)

    # Keyword Matching from Master JSON
    # Hum poore dataset ko scan karte hain keywords ke liye
    def deep_scan(data):
        for key, value in data.items():
            if isinstance(value, list):
                for option in value:
                    if str(option).lower().replace("-", " ") in prompt:
                        build_config["attributes"][key] = option
            elif isinstance(value, dict):
                deep_scan(value)

    deep_scan(MASTER_KNOWLEDGE)

    # Defaults if not found
    if "leg_count" not in build_config["attributes"]:
        build_config["attributes"]["leg_count"] = 4

    params["build_config"] = build_config
    return params