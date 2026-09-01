import json
from typing import Any
from sqlalchemy import inspect


def get_model_column_names(model: Any) -> set[str]:
    
    if hasattr(model, "__table__"):
        return set(model.__table__.columns.keys())
    try:
        insp = inspect(model)
        if hasattr(insp, "mapper"):
            insp = insp.mapper
        return {c.key for c in insp.column_attrs}
    except Exception:
        return set()


def split_model_data(model: Any, raw_data: dict) -> tuple[dict, dict]:
    """
    Splits raw_data dictionary into (model_data, extra_data) based on the model's defined columns.
    """
    model_columns = get_model_column_names(model)
    model_data = {}
    extra_data = {}

    for key, value in raw_data.items():
        if key in model_columns:
            model_data[key] = value
        else:
            extra_data[key] = value

    return model_data, extra_data


def process_model_payload(
    model: Any,
    raw_data: dict,
    existing_extra: str | dict | None = None,
    extra_column_name: str = "additional_details",
) -> dict:

    model_columns = get_model_column_names(model)

    # If the column name on model is additional_data instead of additional_details
    if extra_column_name not in model_columns and "additional_data" in model_columns:
        extra_column_name = "additional_data"

    model_data = {}
    extra_details = {}

    # 1. Parse existing extra data if updating
    if existing_extra:
        if isinstance(existing_extra, dict):
            extra_details.update(existing_extra)
        elif isinstance(existing_extra, str):
            try:
                parsed = json.loads(existing_extra)
                if isinstance(parsed, dict):
                    extra_details.update(parsed)
                else:
                    extra_details["_raw"] = existing_extra
            except Exception:
                extra_details["_raw"] = existing_extra

    # 2. Check if additional_details or additional_data was passed explicitly in raw_data
    passed_details = raw_data.pop("additional_details", None)
    if passed_details is None:
        passed_details = raw_data.pop("additional_data", None)
    else:
        raw_data.pop("additional_data", None)

    if passed_details is not None:
        if isinstance(passed_details, dict):
            extra_details.update(passed_details)
        elif isinstance(passed_details, str):
            try:
                parsed = json.loads(passed_details)
                if isinstance(parsed, dict):
                    extra_details.update(parsed)
                else:
                    extra_details["details"] = parsed
            except Exception:
                extra_details["details"] = passed_details

    # 3. Separate standard model columns from any other keys
    for key, value in raw_data.items():
        if key in model_columns:
            model_data[key] = value
        else:
            extra_details[key] = value

    # 4. Serialize extra keys into extra_column_name as JSON
    if extra_details and extra_column_name in model_columns:
        model_data[extra_column_name] = json.dumps(extra_details)
    elif existing_extra is not None and extra_column_name in model_columns:
        model_data[extra_column_name] = (
            existing_extra if isinstance(existing_extra, str) else json.dumps(existing_extra)
        )

    return model_data
