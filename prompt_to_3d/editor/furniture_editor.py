def apply_edit(params, edit_text):
    edit = edit_text.lower()

    if "thin legs" in edit:
        params.setdefault("components", {}).setdefault("legs", {})
        params["components"]["legs"]["thickness"] = 2

    if "thick legs" in edit:
        params.setdefault("components", {}).setdefault("legs", {})
        params["components"]["legs"]["thickness"] = 6

    return params
