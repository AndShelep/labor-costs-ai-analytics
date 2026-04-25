FROM python:3.12-slim

WORKDIR /app

COPY data_load/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY data_load /app/data_load
COPY data /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "data_load/app.py"]