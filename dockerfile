# Use slim Python 3.12 — smaller image than the full version
FROM python:3.12-slim

# Set working directory inside the container
# All subsequent commands run from here
WORKDIR /app

# Copy requirements first — Docker caches each layer
# If requirements.txt hasn't changed, this layer is cached
# and pip install doesn't re-run on every build
COPY requirements.txt .

# Install dependencies
# --no-cache-dir keeps the image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the source code
# Done after pip install so code changes don't invalidate
# the dependency cache layer
COPY src/ ./src/
COPY .env.example .

# Create the data directory — Chroma and processed files go here
# The actual data comes in via docker-compose volume mount
RUN mkdir -p data/processed/chroma data/raw

# Expose the port uvicorn will listen on
EXPOSE 8000

# Run the app
# --host 0.0.0.0 is important — without it the server only
# listens on localhost inside the container and isn't reachable
CMD ["uvicorn", "src.api.main:app", "--host", "0.0.0.0", "--port", "8000"]