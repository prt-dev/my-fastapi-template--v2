from typing import Any, Optional


def combine_names(
    firstname: Optional[str] = None,
    lastname: Optional[str] = None,
    default_name: Optional[str] = None,
) -> Optional[str]:
    """
    Combines firstname and lastname into a single full name string.
    Returns default_name (or None) if both are empty.
    """
    fname = (firstname or "").strip()
    lname = (lastname or "").strip()
    full_name = f"{fname} {lname}".strip()
    return full_name if full_name else default_name


def split_full_name(full_name: Optional[str]) -> tuple[Optional[str], Optional[str]]:
    """
    Splits a full name string into (firstname, lastname).
    """
    if not full_name or not full_name.strip():
        return None, None
    parts = full_name.strip().split(maxsplit=1)
    firstname = parts[0]
    lastname = parts[1] if len(parts) > 1 else None
    return firstname, lastname


def format_user_names(data: dict, existing_user: Any = None) -> dict:
    
    # Normalize aliases
    if "full_name" in data and "name" not in data:
        data["name"] = data.pop("full_name")
    if "first_name" in data and "firstname" not in data:
        data["firstname"] = data.pop("first_name")
    if "firstName" in data and "firstname" not in data:
        data["firstname"] = data.pop("firstName")
    if "last_name" in data and "lastname" not in data:
        data["lastname"] = data.pop("last_name")
    if "lastName" in data and "lastname" not in data:
        data["lastname"] = data.pop("lastName")

    # Get fallback values if updating an existing user
    existing_fname = getattr(existing_user, "firstname", None) if existing_user else None
    existing_lname = getattr(existing_user, "lastname", None) if existing_user else None
    existing_name = getattr(existing_user, "name", None) if existing_user else None

    fname = data.get("firstname") if data.get("firstname") is not None else existing_fname
    lname = data.get("lastname") if data.get("lastname") is not None else existing_lname

    # Auto-compute 'name' if not explicitly provided or empty
    if not data.get("name"):
        computed_name = combine_names(fname, lname, default_name=existing_name)
        if computed_name:
            data["name"] = computed_name
    elif not data.get("firstname") and not data.get("lastname") and not existing_fname and not existing_lname:
        # If 'name' is provided but firstname/lastname are not, split 'name'
        split_fname, split_lname = split_full_name(data["name"])
        if split_fname and "firstname" not in data:
            data["firstname"] = split_fname
        if split_lname and "lastname" not in data:
            data["lastname"] = split_lname

    return data
