# Use an official Python runtime as a parent image
FROM python:3.8

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /log_processor

# Install dependencies
COPY requirements.txt /log_processor/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . /log_processor/

# Expose port
EXPOSE 8000

# Default command to run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
