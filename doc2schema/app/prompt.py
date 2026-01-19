def build_prompt(text: str, schema: list[str], primary_key: str) -> str:
    return f"""
You are a strict JSON generator.

TASK:
Extract structured data from the document text.

RULES:
- Output ONLY valid JSON
- No markdown, no explanation
- Missing fields must be null
- "{primary_key}" is mandatory
- Skip rows where "{primary_key}" is missing
- Normalize numeric values
- Output must be an array of objects

SCHEMA:
{schema}

DOCUMENT TEXT:
\"\"\"
{text}
\"\"\"
"""


