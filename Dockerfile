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

# Install wheel chatbot_Xsource
RUN pip install ./chat_bot/app/chatbot_Xsource-1.1.0-py3-none-any.whl

# Set working directory for running the application
WORKDIR /usr/src/app/chat_bot

# Set environment variables
ENV OPEN_API_KEY=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

# Make sure the script is executable
RUN chmod +x ./app/main.py

# Define the command to run your application
CMD [ "python", "./app/main.py" ]

# Expose port 8080 for the application
EXPOSE 8080