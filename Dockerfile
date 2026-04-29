# Use full Debian base to avoid apt-get issues
FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED=1
ENV OMP_NUM_THREADS=2

# Install system dependencies needed for PaddleOCR and pdf2image
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        poppler-utils \
        libglib2.0-0 \
        libsm6 \
        libxrender1 \
        libxext6 \
        libgl1-mesa-glx \
        git \
        ca-certificates \
        && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy Python requirements
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy watcher script
COPY watcher.py .

# Create directories for input/output/models
RUN mkdir -p /data/documents /data/ocr_output /tmp /root/.paddleocr

# Default command
CMD ["python", "-u", "watcher.py"]