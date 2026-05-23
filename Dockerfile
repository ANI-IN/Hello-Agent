# Simple container image for the Chat With Your CSV teaching app.
# Build:  docker build -t chat-with-csv .
# Run:    docker run --rm -p 8501:8501 -e OPENAI_API_KEY=sk-... chat-with-csv

FROM python:3.12-slim

# Avoid writing .pyc files and force stdout/stderr to be unbuffered for cleaner logs.
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Install dependencies first so Docker can cache this layer.
COPY requirements.txt ./
RUN pip install -r requirements.txt

# Copy the application source and sample CSVs.
COPY app.py ./
COPY *.csv ./

# Streamlit serves on 8501 by default.
EXPOSE 8501

# Bind to 0.0.0.0 so the port is reachable from outside the container.
CMD ["streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
