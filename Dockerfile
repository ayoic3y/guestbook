FROM python:3.9-alpine
WORKDIR /app
COPY requirements.txt .
RUN apk add --no-cache postgresql-dev gcc python3-dev musl-dev && pip install --no-cache-dir -r requirements.txt
COPY app.py .
CMD ["python", "app.py"]
