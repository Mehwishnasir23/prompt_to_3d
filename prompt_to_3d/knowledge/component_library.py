# Updated to match the new Modular JSON Dataset (v4.0)
FURNITURE_COMPONENTS = {
    "bed": {
        "structural": ["base", "side_rails", "slats"],
        "optional": ["headboard", "footboard", "storage_drawer", "canopy"],
        "quantifiable": ["legs", "storage_drawer"],
        "micro_logic": "sleeping_master_logic"
    },
    "chair": {
        "structural": ["seat", "legs"],
        "optional": ["backrest", "armrest", "headrest", "lumbar_support"],
        "quantifiable": ["legs", "armrest", "swivel_joints_count"],
        "micro_logic": "chair_master_logic"
    },
    "table": {
        "structural": ["table_top", "legs"],
        "optional": ["drawer", "shelf", "cable_grommets", "led_strip_channel"],
        "quantifiable": ["legs", "drawer", "cable_grommets"],
        "micro_logic": "table_master_logic"
    },
    "sofa": {
        "structural": ["base", "legs", "seat_cushion"],
        "optional": ["backrest", "armrest", "cushions", "chaise_longue"],
        "quantifiable": ["legs", "armrest", "cushions"],
        "micro_logic": "sofa_master_logic"
    },
    "cabinet": {
        "structural": ["main_body", "plinth"],
        "optional": ["doors", "shelving", "crown_molding", "kickboard"],
        "quantifiable": ["doors", "shelving", "drawer_count"],
        "micro_logic": "cabinet_master_logic"
    }
}

# Mapping materials from your JSON dataset to HEX/RGB for the Generator
MATERIAL_PROPERTIES = {
    "wood": ["oak", "walnut", "pine", "mahogany", "birch"],
    "fabric": ["velvet", "linen", "leather", "mesh"],
    "metal": ["brushed-steel", "matte-black", "brass", "chrome"],
    "joinery": ["dovetail", "mortise-and-tenon", "cam-lock", "dowel"]
}