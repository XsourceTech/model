# Use a smaller base image for production
FROM python:3.11-slim AS integration

# Create and set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements file into the container
COPY requirements.txt .

# Install Python dependencies from the requirements file
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application code into the container
COPY chat_bot ./chat_bot

RUN pip install ./chat_bot/chatbot_Xsource-1.2.0-py3-none-any.whl

# Set working directory for running the application
WORKDIR /usr/src/app/chat_bot

# Expose port 8080 for the application
EXPOSE 8050

# Define the command to run your application
CMD [ "uvicorn", "app.main:chatbot_app", "--host", "0.0.0.0", "--port", "8050"]
