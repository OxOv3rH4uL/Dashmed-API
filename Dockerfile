FROM python:3.9
LABEL "Project"="Dashmed-Library API"
LABEL "Author"="Pavan"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y git

RUN git clone https://github.com/OxOv3rH4uL/Dashmed-API

RUN pip install --no-cache-dir -r Dashmed-API/requirements.txt

EXPOSE 8000

RUN chmod +x Dashmed-API/startup.sh
CMD ["Dashmed-API/startup.sh"]
