from typing import Any


class dbtToolkitError(Exception):
    def __init__(self, name: str, details: dict[str, Any] = None):
        self.name = name
        self.details = details

    def __str__(self):
        return f"{self.name}: {self.details or '-'}"
