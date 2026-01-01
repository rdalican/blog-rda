# Use Python 3.11 slim image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose port (Railway will override this)
EXPOSE 8000

# Start command
CMD ["gunicorn", "--timeout", "120", "--bind", "0.0.0.0:8000", "blog_app:app"]
