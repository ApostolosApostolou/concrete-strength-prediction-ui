FROM python:3.10-slim

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1

# System deps (if you ever need fonts, certs, etc.)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Python deps
COPY requirements.txt .
RUN pip install -r requirements.txt

# App code
COPY . .

# HF Spaces expects your app to listen on port 8501
ENV PORT=8501
EXPOSE 8501

# Run Streamlit on 0.0.0.0:8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0", "--browser.gatherUsageStats=false"]
