FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app

COPY app/ /app

RUN pip install -r /app/requirements.txt --no-cache-dir

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8085"]