# SchemeSaathi - Production Docker Container
FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000 \
    SCHEMESAATHI_ENV=production

WORKDIR /app

RUN mkdir -p /app/data /app/data/private_vault

COPY . /app/

EXPOSE 8000

CMD ["python", "server.py"]
