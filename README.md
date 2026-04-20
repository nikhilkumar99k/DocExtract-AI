# DocExtract-AI (Doc2Schema)

Convert unstructured documents into structured JSON using OCR + Gemini.

`DocExtract-AI` exposes a FastAPI endpoint that:
- extracts text from PDF, images, Excel, CSV, or TXT
- builds a schema-driven extraction prompt
- uses Gemini to return normalized JSON records

## Why This Project

- Turn raw files into API-ready structured data
- Define your own fields dynamically (no fixed schema in code)
- Handle mixed input formats in one service
- Simple HTTP interface for frontend or automation tools

## Features

- FastAPI backend with a single parse endpoint
- OCR support for images via Tesseract
- PDF text extraction via `pdfplumber`
- Spreadsheet and CSV support via `pandas`
- Gemini model integration for structured extraction
- Chunking for large documents

## Project Structure

```text
DocExtract-AI/
  README.md
  doc2schema/
    requirements.txt
    app/
      main.py         # FastAPI app and /parse endpoint
      extractor.py    # File text extraction (pdf/image/excel/csv/txt)
      gemini.py       # Gemini API call wrapper
      prompt.py       # Prompt template
      utils.py        # Chunking + JSON safety helpers
```

## Requirements

- Python 3.9+
- Tesseract OCR installed on your machine

### Install Tesseract

macOS (Homebrew):

```bash
brew install tesseract
```

Ubuntu/Debian:

```bash
sudo apt-get update
sudo apt-get install -y tesseract-ocr
```

Windows:
- Install from the official Tesseract builds and add it to your PATH.

## Quick Start

From the repository root:

```bash
cd doc2schema
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Server starts at: `http://127.0.0.1:8000`

Swagger docs: `http://127.0.0.1:8000/docs`

## Create a Usable Gemini API Key

1. Open [Google AI Studio](https://aistudio.google.com/app/apikey)
2. Sign in with your Google account
3. Click **Create API key**
4. Copy the generated key and store it safely
5. Use this key as `apiKey` in the `/parse` request

Notes:
- Keep the key private. Never commit it to git.
- If key calls fail, confirm billing/quota status in your Google account.
- Regenerate a new key immediately if it is exposed.

## API Usage

### Endpoint

- `POST /parse`
- Content type: `multipart/form-data`

### Form fields

- `file` (required): input document file
- `primaryKey` (required): unique field name to keep mandatory
- `fields` (required): comma-separated schema fields
- `apiKey` (required): Gemini API key

### Supported file types

- `.pdf`
- `.png`, `.jpg`, `.jpeg`
- `.xls`, `.xlsx`
- `.csv`
- `.txt`

### Example cURL

```bash
curl -X POST "http://127.0.0.1:8000/parse" \
  -F "file=@/absolute/path/to/invoice.pdf" \
  -F "primaryKey=invoice_id" \
  -F "fields=invoice_id,customer_name,total,invoice_date" \
  -F "apiKey=YOUR_GEMINI_API_KEY"
```

### Example response

```json
{
  "primaryKey": "invoice_id",
  "count": 2,
  "data": [
    {
      "invoice_id": "INV-1001",
      "customer_name": "Acme Corp",
      "total": 1499.5,
      "invoice_date": "2026-03-15"
    }
  ]
}
```

## Common Errors

- `400 primaryKey is required`: missing `primaryKey`
- `400 fields is required`: missing `fields`
- `400 apiKey is required`: missing Gemini key
- `400 File extension missing`: file has no extension
- `422 No extractable text found`: OCR/text extraction returned empty

## Open Source Contribution Guide

1. Fork the repository
2. Create a feature branch
3. Make focused changes with clear commit messages
4. Add or update tests when relevant
5. Open a pull request describing the problem and fix

Suggested branch naming:
- `feature/<short-name>`
- `fix/<short-name>`

## Security Best Practices

- Never hardcode API keys in source files
- Do not upload sensitive documents to public environments
- Rotate keys regularly
- Use `.gitignore` for local secrets and temporary files

## License

Add a `LICENSE` file (for example MIT) before public release.
