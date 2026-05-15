FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# Install system build deps required to compile/install MuPDF/PyMuPDF and Tesseract
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential gcc g++ cmake pkg-config \
    libfreetype6-dev libjpeg-dev libopenjp2-7-dev libtiff-dev zlib1g-dev libpng-dev \
    libfontconfig1-dev libx11-dev libxcb1-dev libxrender-dev \
    tesseract-ocr libleptonica-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy only backend requirements first for better caching
COPY backend/requirements.txt /app/backend/requirements.txt
WORKDIR /app/backend

# Upgrade packaging tools and install Python deps
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source
COPY backend /app/backend

EXPOSE 8000

# Start the FastAPI app; use PORT env var if provided by host/platform
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-8000}"]
