FROM python:3.12-slim

# Устанавливаем Firefox и необходимые библиотеки
RUN apt-get update && apt-get install -y firefox-esr --no-install-recommends && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install --no-cache-dir -r requirements.txt
CMD ["python", "-m", "pytest", "-v"]
