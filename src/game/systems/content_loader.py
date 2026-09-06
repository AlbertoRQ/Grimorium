"""Carga el contenido de tienda exportado desde el libro maestro.

El juego solo lee JSON. El Excel se usa como herramienta de autoria mediante
``tools/export_content.py`` y nunca forma parte del bucle de juego.
"""

from __future__ import annotations

import json
from collections import defaultdict
from typing import Any

from game.utils.paths import data_path


def _load_json(filename: str) -> list[dict[str, Any]]:
    path = data_path("game", filename)
    with path.open("r", encoding="utf-8") as file:
        value = json.load(file)
    if not isinstance(value, list):
        raise ValueError(f"{path} debe contener una lista")
    return value


def _coerce_effect_value(effect: dict[str, Any]) -> Any:
    value = effect.get("value")
    if effect.get("value_type") == "bool":
        return bool(value)
    return value


def load_shop_content():
    """Devuelve ``POTION_DATA``, ``POWER_DATA`` y ``BOOK_DATA``.

    Las filas desactivadas siguen documentadas en los JSON, pero no entran en
    la tienda. Esto permite conservar borradores sin activarlos por accidente.
    """

    items = _load_json("items.json")
    effects = _load_json("effects.json")

    effects_by_owner: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for effect in effects:
        effects_by_owner[(effect["owner_type"], effect["owner_id"])].append(effect)

    potions: dict[str, dict[str, Any]] = {}
    powers: dict[str, dict[str, Any]] = {}
    books: dict[str, dict[str, Any]] = {}

    for item in items:
        if not item.get("enabled", False):
            continue

        item_type = item["type"]
        item_id = item["id"]
        common = {
            "text_key": item["text_key"],
            "price": item["price"],
            "asset": item["asset"],
        }
        if item.get("tooltip_style"):
            common["tooltip_style"] = item["tooltip_style"]

        if item.get("is_plus", False):
            common["is_plus"] = True

        owned_effects = effects_by_owner[(item_type, item_id)]

        if item_type == "potion":
            if len(owned_effects) != 1:
                raise ValueError(f"La pocion {item_id} debe tener exactamente un efecto")
            effect = owned_effects[0]
            potions[item_id] = {
                **common,
                "stat": effect["target"],
                "amount": _coerce_effect_value(effect),
            }
            continue

        if item_type == "power":
            category = item.get("category") or "element"
            if category == "shot_modifier":
                modifier = {}
                for effect in owned_effects:
                    modifier[effect["target"]] = {
                        "operation": effect["operation"],
                        "value": _coerce_effect_value(effect),
                    }
                powers[item_id] = {
                    **common,
                    "category": category,
                    "modifier": modifier,
                }
            else:
                powers[item_id] = {
                    **common,
                    "category": category,
                    "mode": item["mode"],
                    "element": item["target_id"],
                    "chance": item["chance"],
                }
            continue

        if item_type == "book":
            scope_key = item["category"]
            effect_data = {scope_key: item["target_id"]}
            effect_units = {}
            for effect in owned_effects:
                target = effect["target"]
                effect_data[target] = _coerce_effect_value(effect)
                effect_units[target] = effect.get("unit")
            books[item_id] = {
                **common,
                "effect": effect_data,
                "effect_units": effect_units,
            }
            continue

        raise ValueError(f"Tipo de objeto desconocido: {item_type}")

    return potions, powers, books
