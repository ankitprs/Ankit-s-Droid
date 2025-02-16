FROM python:3.8-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Expose the port FastAPI runs on
EXPOSE 8000

# Command to run the application