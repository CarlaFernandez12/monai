FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY api /app/api

ENV PYTHONPATH="/app"

EXPOSE 5000

CMD ["python", "api/app.py"]
