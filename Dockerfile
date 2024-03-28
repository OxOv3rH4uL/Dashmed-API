FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/OxOv3rH4uL/Django-API


RUN pip install --no-cache-dir -r Django-API/requirements.txt

EXPOSE 8000

RUN chmod +x Django-API/startup.sh
CMD ["Django-API/startup.sh"]
