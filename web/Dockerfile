FROM python:3.12-slim

WORKDIR /app

COPY web/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY web /app/web

ENV PYTHONUNBUFFERED=1

EXPOSE 5000

CMD ["python", "web/app.py"]