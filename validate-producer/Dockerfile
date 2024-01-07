# Set python version
ARG BASE_CONTAINER=python:3.8

# Set the base image 
FROM --platform=linux/amd64 $BASE_CONTAINER

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

# Sets the user name to use when running the image.
USER root
RUN apt update && \
    apt install --no-install-recommends -y build-essential gcc && \
    apt clean && rm -rf /var/lib/apt/lists/*

# Make a directory for our app
WORKDIR /validate-producer

# Install dependencies
COPY requirements.txt .

RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy source code and startup script
COPY ./app ./app
COPY startup.sh .

# Give execute permissions to the startup script
RUN chmod +x startup.sh

# Set the startup script as the entry point
CMD ["./startup.sh"]
