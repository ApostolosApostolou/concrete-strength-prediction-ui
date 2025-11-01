# Dockerfile
FROM python:3.10-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app
ENV PIP_NO_CACHE_DIR=1

# System deps
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Install Python deps first
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY . .

# Cloud Run Port
ENV PORT=8080
EXPOSE 8080

# Drop privileges
USER appuser

# Start Streamlit
CMD ["sh","-c","streamlit run app.py --server.address=0.0.0.0 --server.port=${PORT} --browser.gatherUsageStats=false"]
