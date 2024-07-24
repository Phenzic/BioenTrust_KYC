FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt /app/

RUN python3 -m venv venv \
    && /app/venv/bin/pip install --no-cache-dir -r requirements.txt


RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

CMD ["/app/venv/bin/python", "wsgi.py"]

EXPOSE 5000
