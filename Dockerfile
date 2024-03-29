FROM python:3.9
LABEL "Project"="Dashmed-Library API"
LABEL "Author"="Pavan"

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MYSQL_DATABASE=dashmed

RUN apt-get update && apt-get install -y git

RUN apt-get update && apt-get install -y git wget mariadb-server mariadb-client libmariadb-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/*

RUN service mariadb start && \
    mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"


RUN git clone https://github.com/OxOv3rH4uL/Django-API

RUN pip install --no-cache-dir -r Django-API/requirements.txt

EXPOSE 8000

RUN chmod +x Django-API/startup.sh
CMD ["Django-API/startup.sh"]
