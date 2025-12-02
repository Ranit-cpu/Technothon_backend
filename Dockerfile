FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y gcc libmariadb-dev && rm -rf /var/lib/apt/lists/*

COPY req.txt req.txt

RUN pip3 install -r req.txt

FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y gcc libmariadb-dev && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY req.txt req.txt
RUN pip3 install -r req.txt

# Copy db.py and other app files
COPY db.py .
COPY . .

# Run db.py to initialize DB
RUN python3 db.py

# Copy app files
COPY . .

# Expose FastAPI port
EXPOSE 8000

# Run the FastAPI app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
