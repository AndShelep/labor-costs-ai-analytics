FROM python:3.12-slim

WORKDIR /app

COPY data_quality_analysis/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY data_quality_analysis /app/data_quality_analysis
COPY data /app/data

ENV PYTHONUNBUFFERED=1

CMD ["python", "data_quality_analysis/app.py"]