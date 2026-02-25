# Use the official Python image as the base image
FROM python:3.9-slim

# Set environment variables
ENV GCP_PROJECT="temp" \
    GCP_PROJECT_ID="temp-416704" \
    PUBSUB_TOPIC_NEW_PRODUCT="new-product" \
    PUBSUB_TOPIC_PAYMENT_PROCESS="payment-process" \
    GCS_BUCKET="temp-image-111" \
    FIREBASE_CONFIG="firebase_config.json" \
    API_GATEWAY_URL="" \
    JWT_EMAIL=""

# Set the working directory in the container
WORKDIR /app

# Copy the app directory to the working directory in the container
COPY app/ .

# Install any dependencies
COPY app/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 80 to the outside world
EXPOSE 5000

# Command to run the Flask application
CMD ["python", "main.py"]