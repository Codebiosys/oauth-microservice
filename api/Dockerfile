#
# Dockerfile for testing API service
#

FROM python:3.6

# Declare application root for easier copying of files
WORKDIR /app

# Copy version specs first so they can be cached by Docker
COPY requirements.txt ./
COPY dev_requirements.txt ./
RUN pip install -r requirements.txt && pip install -r dev_requirements.txt

RUN pip install gunicorn

# Copy source code last so it can be mounted in Compose
COPY . .

# Default command to get the application up and running
CMD ["bash", "docker_entrypoint.sh"]
