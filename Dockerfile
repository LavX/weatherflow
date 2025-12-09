FROM python:3.14-slim

# Set the working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY src/ ./src/

# Set Python path
ENV PYTHONPATH=/app

# Run the application
CMD ["python", "-m", "src.main"]