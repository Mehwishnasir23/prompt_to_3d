import re

# -----------------------------
# Keyword Dictionaries
# -----------------------------

FURNITURE_TYPES = [
    "chair", "table", "sofa", "bed", "cabinet", "cupboard", "shelf"
]

MATERIALS = ["wood", "metal", "plastic", "fabric", "glass"]

COLORS = ["white", "black", "brown", "gray", "grey", "oak"]

STYLES = ["modern", "classic", "minimal", "luxury", "japanese", "scandinavian"]

# -----------------------------
# Helper Functions
# -----------------------------

def find_keyword(text, keywords):
    """Return first keyword found in text"""
    for word in keywords:
        if word in text:
            return word
    return None


def find_number_before_word(text, word):
    """
    Example:
    'sofa with 3 seats' → returns 3
    """
    pattern = rf"(\d+)\s+{word}"
    match = re.search(pattern, text)
    if match:
        return int(match.group(1))
    return None


# -----------------------------
# Main Prompt Parser
# -----------------------------

def parse_prompt(prompt: str) -> dict:
    """
    Converts user prompt into structured parameters
    (Hybrid AI ready: preserves raw prompt for semantic reasoning)
    """

    text = prompt.lower()

    result = {
        "furniture_type": None,
        "category": None,
        "style": None,
        "dimensions": {},
        "components": {},
        "material": {},
        "colors": {},
        "features": {}
    }

    # -----------------------------
    # Furniture Type
    # -----------------------------
    furniture = find_keyword(text, FURNITURE_TYPES)
    if furniture:
        result["furniture_type"] = furniture

        if furniture in ["chair", "sofa"]:
            result["category"] = "seating"
        elif furniture in ["table"]:
            result["category"] = "surface"
        elif furniture in ["bed"]:
            result["category"] = "sleeping"
        else:
            result["category"] = "storage"

    # -----------------------------
    # Style
    # -----------------------------
    style = find_keyword(text, STYLES)
    if style:
        result["style"] = style

    # -----------------------------
    # Material
    # -----------------------------
    material = find_keyword(text, MATERIALS)
    if material:
        result["material"]["primary"] = material

    # -----------------------------
    # Colors
    # -----------------------------
    for color in COLORS:
        if color in text:
            result["colors"]["body"] = color
            break

    # -----------------------------
    # Components Logic
    # -----------------------------

    # Legs
    leg_count = find_number_before_word(text, "legs")
    if leg_count:
        result["components"]["legs"] = {"count": leg_count}

    if "short legs" in text:
        result["components"].setdefault("legs", {})
        result["components"]["legs"]["height"] = "short"

    if "long legs" in text:
        result["components"].setdefault("legs", {})
        result["components"]["legs"]["height"] = "long"

    # Seats (for sofa)
    seats = find_number_before_word(text, "seats")
    if seats:
        result["components"]["seats"] = seats

    # Backrest
    if "backrest" in text or "with back" in text:
        result["components"]["backrest"] = True

    if "no backrest" in text:
        result["components"]["backrest"] = False

    # Armrest
    if "armrest" in text:
        result["components"]["armrest"] = True

    if "no armrest" in text:
        result["components"]["armrest"] = False

    # Storage / Drawers
    if "drawer" in text or "storage" in text:
        result["features"]["storage"] = True

    # Height semantics (learning-like)
    if "low height" in text or "low profile" in text:
        result["dimensions"]["height"] = "low"

    if "high" in text or "tall" in text:
        result["dimensions"]["height"] = "high"

    # -----------------------------
    # 🔴 Preserve Raw Prompt (IMPORTANT)
    # -----------------------------
    result["raw_prompt"] = prompt

    # -----------------------------
    # Clean Empty Fields
    # -----------------------------
    result = {k: v for k, v in result.items() if v not in [None, {}, []]}

    return result


# -----------------------------
# Testing (Run directly)
# -----------------------------
if __name__ == "__main__":
    test_prompts = [
        "White wooden chair with 4 legs and backrest",
        "Modern sofa with 3 seats and short legs",
        "Classic wooden table with 4 legs",
        "Low height Japanese style bed with storage and no headboard",
        "Black metal cabinet with shelves"
    ]

    for p in test_prompts:
        print("\nPROMPT:", p)
        print("OUTPUT:", parse_prompt(p))
