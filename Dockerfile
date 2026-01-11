FROM python:3.11-slim

WORKDIR /app

# Copy backend only
COPY backend/ ./backend/

# Install deps
RUN python -m pip install --upgrade pip setuptools wheel \
    && python -m pip install -r backend/requirements.txt

# Run FastAPI
CMD ["python", "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080", "--app-dir", "backend"]
