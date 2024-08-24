# Use a smaller base image for production
FROM python:3.11-slim AS integration

# Create and set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY chat_bot/app ./chat_bot/app

RUN pip install --use-wheel --no-index --find-links=./chat_bot/chatbot_Xsource-1.1.0-py3-none-any.whl

# Copy the entire application code into the container
ARG ENVIRONMENT
COPY .env.${ENVIRONMENT} .env

# Set working directory for running the application
WORKDIR /usr/src/app/chat_bot

# Make sure the script is executable
RUN chmod +x ./app/main.py

# Define the command to run your application
CMD [ "python", "./app/main.py" ]

# Expose port 8080 for the application
EXPOSE 8080