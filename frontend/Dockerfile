FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libjpeg-dev \
    libopenjp2-7-dev \
    libtiff-dev \
    zlib1g-dev \
    libpng-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt /app/requirements.txt

# Install Python dependencies
RUN python -m pip install --upgrade pip setuptools wheel

RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy frontend source code
COPY . /app

EXPOSE 8501

# Start Streamlit app
CMD ["sh", "-c", "streamlit run streamlit_app.py --server.port ${PORT:-8501} --server.address 0.0.0.0"]