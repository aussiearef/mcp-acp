FROM python:alpine3.21
WORKDIR /app
RUN pip install --no-cache-dir fastmcp
COPY server.py .
EXPOSE 8000
CMD ["python", "server.py"]
