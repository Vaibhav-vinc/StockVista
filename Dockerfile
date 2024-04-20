# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables for Python
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory to /code
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy only the requirements file
COPY requirements.txt /code/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Collect static files
RUN python manage.py collectstatic --noinput

# Expose the port that the app will run on
EXPOSE 8000

# Run the application using Gunicorn (recommended for production)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "stockvista.wsgi:application"]
