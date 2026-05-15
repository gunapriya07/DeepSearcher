FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive
WORKDIR /app

# System deps for common Python imaging/data packages used by Streamlit
RUN apt-get update \
  && apt-get install -y --no-install-recommends \
    build-essential libjpeg-dev libopenjp2-7-dev libtiff-dev zlib1g-dev libpng-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy and install frontend Python dependencies
COPY frontend/requirements.txt /app/requirements.txt
RUN python -m pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy app sources
COPY frontend /app

EXPOSE 8501

# Run Streamlit (use PORT env var if provided)
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]
