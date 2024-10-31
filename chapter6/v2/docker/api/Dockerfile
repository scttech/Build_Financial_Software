# Using the latest version of python
FROM python:alpine

# Set the working directory to /code
WORKDIR /code

# Copy the requirements.txt file to the working directory
COPY ./requirements.txt /code/requirements.txt

# Install any needed packages specified in requirements.txt
RUN apk -U upgrade
RUN apk add --no-cache libpq-dev python3-dev gcc musl-dev
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy our app code to the working directory
COPY ./app /code/app
COPY ./ach_processor /code/ach_processor

ENV PYTHONPATH /code

# Star the application using uvicorn
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
