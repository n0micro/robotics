# Використовуємо офіційний образ Python
FROM python:3.9-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли залежностей
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь проєкт
COPY . .

# Встановлюємо змінну середовища для порту (Cloud Run задасть PORT автоматично)
ENV PORT=3000

# Запускаємо додаток
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 server:app