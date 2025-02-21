# Use official Python image
FROM python:3.10

# Set working directory
WORKDIR /app

# Install dependencies
COPY ../requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt gunicorn

# Copy Django project
COPY ../ /app/

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Run migrations before starting Gunicorn
CMD ["sh", "-c", "python manage.py makemigrations && python manage.py migrate && gunicorn --bind 0.0.0.0:8000 backend.wsgi:application"]
