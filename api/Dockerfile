FROM tiangolo/uvicorn-gunicorn

# Set the working directory to /app
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Create the api directory and copy the contents
# This ensures that 'import api.server' works from /app
COPY . ./api

# Set PYTHONPATH to include the current directory
ENV PYTHONPATH=/app

# Expose the port
EXPOSE 8000

# Start uvicorn. We point to the module 'api.server'
CMD ["uvicorn", "api.server:app", "--host", "0.0.0.0", "--port", "8000"]
