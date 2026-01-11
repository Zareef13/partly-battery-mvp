# Partly Battery MVP

Minimal FastAPI backend for battery content enrichment.

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
cd backend
pip install -r requirements.txt
```

3. Copy `.env.example` to `.env` and optionally add your Gemini API key:
```bash
cp ../.env.example ../.env
# Edit .env and add GEMINI_API_KEY if you have one
```

4. Run the server:
```bash
./run.sh
# Or: uvicorn app.main:app --reload --port 8000
```

Server will start at `http://localhost:8000`

## API Endpoints

### Health Check
```bash
curl http://localhost:8000/health
```

### Upload File
```bash
curl -X POST "http://localhost:8000/upload" \
  -F "file=@data/demo_input.csv"
```

### Enrich Batteries
```bash
curl -X POST "http://localhost:8000/enrich" \
  -H "Content-Type: application/json" \
  -d '{
    "items": [
      {"mpn": "CR2032", "manufacturer": "Panasonic"},
      {"mpn": "18650", "manufacturer": "Samsung"}
    ]
  }'
```

### Export to Jameco Format
```bash
curl -X POST "http://localhost:8000/export" \
  -H "Content-Type: application/json" \
  -d '{
    "records": [...],
    "format": "xlsx"
  }' \
  --output output.xlsx
```

## Demo

A sample input file is provided at `data/demo_input.csv`. You can use it to test the upload endpoint.

## Notes

- Caching: Enriched data is cached at `data/cache/<mpn>.json` to avoid redundant processing
- Gemini: Optional - if `GEMINI_API_KEY` is not set, overviews are generated from extracted fields
- Data fetching: Currently uses stub data for demo purposes. Real search/scraping can be swapped in later.

