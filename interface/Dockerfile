FROM python:3.10-slim

# We'll install dependencies for the UI
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy app code
COPY app.py .

# Expose Flask's default port
EXPOSE 5000

# Launch the Flask app
CMD ["python", "app.py"]