FROM python:3.12-slim

WORKDIR /app

COPY visualization/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY visualization /app/visualization
COPY data /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "visualization/app.py"]