# 1. Base image
FROM python:3.11-slim

# 2. Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# 3. Create & set workdir
WORKDIR /app

# 4. Install system dependencies (if you need e.g. gcc for packages)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
      build-essential \
 && rm -rf /var/lib/apt/lists/*

# 5. Install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt

# 6. Copy project code
COPY . .

# 7. Collect static files (if you have any)
# RUN python manage.py collectstatic --no-input

# 8. Expose port (Django’s default)
EXPOSE 8000

# 9. Run migrations then start the server
#    For development you can use runserver; for production swap to gunicorn
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]

