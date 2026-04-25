FROM python:3.12-slim

WORKDIR /app

COPY data_research/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY data_research /app/data_research
COPY data /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "data_research/app.py"]