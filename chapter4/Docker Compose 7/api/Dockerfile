# Using the latest version of python
FROM python:latest

# Set the working directory to /code
WORKDIR /code

# Copy the requirements.txt file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
# --no-cache-dir: disable the cache for pip, so they are not stored in the docker container
# --upgrade: upgrade all the packages to the latest version
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy our app code to the working directory
COPY ./app /code/app

# Star the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
