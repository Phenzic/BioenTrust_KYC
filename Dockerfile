FROM python:3.10

WORKDIR /app

COPY . /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_ENV=production

CMD ["python", "app.py"]
