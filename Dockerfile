FROM python:3.9-slim

# Create and use a non-root user 
RUN useradd --create-home appuser
WORKDIR /app
USER appuser

COPY server/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the server code
COPY server/ .

EXPOSE 9999

CMD ["python", "server.py"]