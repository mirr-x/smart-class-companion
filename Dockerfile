# Use Python 3.13 slim image
FROM python:3.13-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV USE_ORACLE=true

# Set work directory
WORKDIR /app

# Install system dependencies
# libaio1 is often needed for Oracle, though thin mode avoids it, it's safer to have basic libs.
# netcat/curl for checking db readiness if we add a wait-for-it script later.
RUN apt-get update && apt-get install -y \
    gettext \
    libaio1 \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Install python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project
COPY . /app/

# Expose port (not strictly needed for compose but good documentation)
EXPOSE 8000

# Default command (can be overridden in compose)
# We will use the development server as requested for "running all this"
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
