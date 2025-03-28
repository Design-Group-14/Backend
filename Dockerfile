# Use official Python image
FROM python:3.11-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create working directory
WORKDIR /code

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY backend/ .

# Expose port
EXPOSE 8000

# Run Gunicorn server
CMD ["gunicorn", "tcd_social.wsgi:application", "--bind", "0.0.0.0:8000"]