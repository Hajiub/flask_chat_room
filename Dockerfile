# Use a lightweight Python 3 base image
FROM python:3-alpine

# Set the working directory to /app
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt ./

# Install the required packages
RUN apk add --no-cache --virtual .build-deps gcc musl-dev && \
    pip install --no-cache-dir -r requirements.txt && \
    apk del .build-deps gcc musl-dev

# Copy the application code to the container
COPY . .

# Expose the port used by the application
EXPOSE 5000

# Set the environment variable for the Flask app
ENV FLASK_APP=app.py

# Run the Flask app when the container starts
CMD ["flask", "run", "--host=0.0.0.0"]
