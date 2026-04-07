# Sinamor's lightweight Docker config
FROM python:3.11-slim

# Prevent cache building up & stream outputs to console instantly
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    STREAMLIT_SERVER_PORT=8501

WORKDIR /app

# Install system-level audio dependencies (for pyaudio / pyttsx3)
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    libasound-dev \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Install python packages (disabling cache for smaller image footprint)
RUN pip install --no-cache-dir -r requirements.txt

# Copy our app's source
COPY . /app

EXPOSE 8501

# Streamlit cloud-native health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Launch 🚀
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
