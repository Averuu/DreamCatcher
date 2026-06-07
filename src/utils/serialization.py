"""
Утилиты для сериализации/десериализации данных в JSON.
"""
import json
import os

def save_game(data: dict, path: str = "data/save.json") -> None:
    """Сохраняет словарь data в JSON-файл."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_game(path: str = "data/save.json") -> dict:
    """Загружает данные из JSON-файла. Если файла нет, возвращает пустой словарь."""
    if not os.path.exists(path):
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)