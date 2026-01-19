from typing import List

from pydantic import BaseModel


class SchemaInput(BaseModel):
    primaryKey: str
    fields: List[str]


