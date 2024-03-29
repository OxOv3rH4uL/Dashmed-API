FROM python:3.9

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=dashmed
ENV MYSQL_PORT=3307

RUN apt-get update && apt-get install -y git
RUN apt-get update && apt-get install -y \
    mysql-server \
    libmysqlclient-dev

RUN service mysql start \
    && mysql -u root -proot -e "CREATE DATABASE IF NOT EXISTS $MYSQL_DATABASE;"

RUN sed -i "s/bind-address.*/bind-address = 0.0.0.0/" /etc/mysql/mysql.conf.d/mysqld.cnf \
    && sed -i "s/port.*/port = $MYSQL_PORT/" /etc/mysql/mysql.conf.d/mysqld.cnf

RUN apt-get install -y mysql-client

RUN git clone https://github.com/OxOv3rH4uL/Django-API

RUN pip install --no-cache-dir -r Django-API/requirements.txt

EXPOSE 8000

RUN chmod +x Django-API/startup.sh
CMD ["Django-API/startup.sh"]
