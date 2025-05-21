FROM python:3.10-slim

WORKDIR /app

# Install system dependencies (optional: for PIL or SSL issues)
RUN apt-get update && apt-get install -y \
    libglib2.0-0 libsm6 libxext6 libxrender-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy and install Python dependencies
COPY backend/requirements.txt ./
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy app and dependencies
COPY backend/app/ app/
COPY embeddings/ embeddings/

# Run API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
