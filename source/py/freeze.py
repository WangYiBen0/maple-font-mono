from source.py.in_browser import (
    freeze_feature as freeze,
    MOVING_RULES as default_moving_rules,
    get_freeze_config_str as config_str,
)
from fontTools.ttLib import TTFont


def is_enable(v):
    return v.upper().startswith("ENABLE")


def is_disable(v):
    return v.upper().startswith("DISABLE")


def is_ignore(v):
    return v.upper().startswith("IGNORE")


def parse_config(config: dict, calt: bool):
    result = {}
    invalid_items = []
    for k, v in config.items():
        if is_enable(v):
            result[k] = "1"
        elif is_disable(v):
            result[k] = "0"
        elif not is_ignore(v):
            invalid_items.append((k, v))

    if len(invalid_items) > 0:
        report = ", ".join([f"{k}: {v}" for k, v in invalid_items])
        raise TypeError(f"Invalid freeze config item: {{ {report} }}")

    result["calt"] = "1" if calt else "0"

    return result


def get_freeze_config_str(config: dict, calt: bool) -> str:
    return config_str(parse_config(config, calt))


def freeze_feature(font: TTFont, calt: bool, moving_rules: list[str], config: dict):
    return freeze(
        font, moving_rules or default_moving_rules, parse_config(config, calt)
    )
