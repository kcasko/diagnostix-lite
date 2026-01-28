# DiagnOStiX - Cross-Platform Diagnostic Tool
FROM python:3.12-slim

# Install system tools for enhanced diagnostics
RUN apt-get update && apt-get install -y \
    bash \
    smartmontools \
    net-tools \
    iputils-ping \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY webui/requirements.txt ./webui/
RUN pip install --no-cache-dir -r ./webui/requirements.txt

# Copy application files
COPY webui/ ./webui/
COPY scripts/ ./scripts/
COPY branding/ ./branding/

# Make scripts executable
RUN chmod +x scripts/*.sh

# Expose port
EXPOSE 8000

# Set working directory to webui
WORKDIR /app/webui

# Run with uvicorn
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
