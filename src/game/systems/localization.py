import json

from game.utils.paths import data_path


class Localization:
    def __init__(self, language="es"):
        self.language = language
        self.texts = {}
        self.load(language)

    def load(self, language):
        self.language = language

        path = data_path("lang", f"{language}.json")
        with open(path, "r", encoding="utf-8") as file:
            self.texts = json.load(file)

    def text(self, key, fallback=None):
        if fallback is None:
            fallback = key

        value = self.texts

        for part in key.split("."):
            if not isinstance(value, dict) or part not in value:
                return fallback

            value = value[part]

        return value