FROM python:3.11-slim

# Install LibreOffice and other system dependencies
RUN apt-get update && apt-get install -y \
    libreoffice \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create necessary directories
RUN mkdir -p uploads converted output

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_ENV=production
ENV SECRET_KEY=change-this-in-production

# Run the application
CMD ["python", "app.py"]
