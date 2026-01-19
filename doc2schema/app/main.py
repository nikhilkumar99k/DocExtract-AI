import os
from tempfile import NamedTemporaryFile
from typing import Annotated

from fastapi import FastAPI, File, Form, HTTPException, UploadFile
from fastapi.middleware.cors import CORSMiddleware

from app.extractor import extract_text
from app.gemini import call_gemini
from app.prompt import build_prompt
from app.utils import chunk_text, safe_json


app = FastAPI(title="Doc2Schema")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/parse")
async def parse_document(
    file: UploadFile = File(...),
    primaryKey: Annotated[str, Form(...)] = "",
    fields: Annotated[str, Form(...)] = "",
    apiKey: Annotated[str, Form(...)] = "",
):
    # -----------------------
    # Validate inputs
    # -----------------------
    if not primaryKey:
        raise HTTPException(status_code=400, detail="primaryKey is required")

    if not fields:
        raise HTTPException(status_code=400, detail="fields is required")

    if not file.filename:
        raise HTTPException(status_code=400, detail="Invalid file")
    
    if not apiKey:
        raise HTTPException(status_code=400, detail="apiKey is required")
        

    # -----------------------
    # Prepare schema
    # -----------------------
    schema_fields = [f.strip() for f in fields.split(",") if f.strip()]
    if primaryKey not in schema_fields:
        schema_fields.insert(0, primaryKey)

    # -----------------------
    # Preserve file extension
    # -----------------------
    _, ext = os.path.splitext(file.filename)
    if not ext:
        raise HTTPException(status_code=400, detail="File extension missing")

    with NamedTemporaryFile(delete=False, suffix=ext) as tmp:
        tmp.write(await file.read())
        tmp_path = tmp.name

    try:
        # -----------------------
        # Extract text
        # -----------------------
        raw_text = extract_text(tmp_path)

        if not raw_text.strip():
            raise HTTPException(status_code=422, detail="No extractable text found")

        chunks = chunk_text(raw_text)

        results = []

        # -----------------------
        # AI parsing
        # -----------------------
        for chunk in chunks:
            if not chunk.strip():
                continue

            prompt = build_prompt(
                text=chunk,
                schema=schema_fields,
                primary_key=primaryKey,
            )

            parsed = call_gemini(prompt, apiKey)
            parsed_list = safe_json(parsed)
            results.extend(parsed_list)

        return {
            "primaryKey": primaryKey,
            "count": len(results),
            "data": results,
        }

    finally:
        if os.path.exists(tmp_path):
            os.remove(tmp_path)
