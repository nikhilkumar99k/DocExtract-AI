import json
from typing import Any, List

from jsonschema import ValidationError, validate  # noqa: F401


MAX_CHARS = 12000


def chunk_text(text: str) -> List[str]:
    if not text:
        return []
    return [text[i : i + MAX_CHARS] for i in range(0, len(text), MAX_CHARS)]


def safe_json(output: Any):
    if isinstance(output, list):
        return output
    try:
        parsed = json.loads(output)
    except Exception as exc:
        raise ValueError("Invalid JSON output") from exc
    if isinstance(parsed, list):
        return parsed
    raise ValueError("Invalid JSON output")


