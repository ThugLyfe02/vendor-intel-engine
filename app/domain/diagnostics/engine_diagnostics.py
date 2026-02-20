from typing import Dict, Any


class EngineDiagnostics:

    VERSION = "1.0.0"

    def __init__(self):
        self.warnings = []
        self.errors = []

    def add_warning(self, message: str):
        self.warnings.append(message)

    def add_error(self, message: str):
        self.errors.append(message)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "diagnostics_version": self.VERSION,
            "warnings": self.warnings,
            "errors": self.errors,
        }
