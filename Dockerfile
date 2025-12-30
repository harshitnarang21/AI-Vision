FROM python:3.13-slim

# Install system dependencies for OpenCV (libGL.so.1) and friends
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

# Create virtualenv and install Python deps
RUN python -m venv .venv \
 && . .venv/bin/activate \
 && pip install --upgrade pip \
 && pip install -r requirements.txt

ENV PYTHONUNBUFFERED=1
ENV PORT=8000

CMD