# Use Python image
FROM python:3.12

# Set working directory
WORKDIR /app

# Copy requirements and install them
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Expose the Flask port
EXPOSE 1234

# Run the Flask application
CMD ["flask", "run", "--host=0.0.0.0", "--port=1234"]
