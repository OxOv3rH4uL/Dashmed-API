    FROM python:3.9

    ENV PYTHONDONTWRITEBYTECODE 1
    ENV PYTHONUNBUFFERED 1

    RUN apt-get update && apt-get install -y git

    RUN git clone https://github.com/OxOv3rH4uL/Django-API

    COPY requirements.txt .

    RUN pip install --no-cache-dir -r requirements.txt

    EXPOSE 8000

    COPY start.sh /
    RUN chmod +x /start.sh
    CMD ["/start.sh"]
