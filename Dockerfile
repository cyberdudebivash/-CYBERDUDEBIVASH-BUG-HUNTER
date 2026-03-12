# Stage 1: Build Dependencies
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Stage 2: Final Production Image
FROM python:3.12-slim
WORKDIR /app

# Install runtime dependencies for DNS/Recon tools
RUN apt-get update && apt-get install -y --no-cache-dir \
    dnsutils \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed packages from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy the entire platform structure
COPY . .

# Set environment to production
ENV PYTHONUNBUFFERED=1
ENV API_ENV=production

# Default command is overridden by docker-compose for different services
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]