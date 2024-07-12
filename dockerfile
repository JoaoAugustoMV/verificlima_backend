FROM python:3.10-slim-bullseye
WORKDIR /fastapi
COPY requirements.txt /fastapi

RUN apt update && apt install -y pkg-config gcc \
    default-libmysqlclient-dev pkg-config 

RUN apt-get update \
    && apt-get install unixodbc -y \
    && apt-get install unixodbc-dev -y \
    && apt-get install freetds-dev -y \
    && apt-get install freetds-bin -y \
    && apt-get install tdsodbc -y \
    && apt-get install --reinstall build-essential -y


RUN apt-get -y install curl
RUN curl https://packages.microsoft.com/keys/microsoft.asc | apt-key add -
RUN curl https://packages.microsoft.com/config/debian/11/prod.list > /etc/apt/sources.list.d/mssql-release.list

RUN apt-get update
RUN env ACCEPT_EULA=Y apt-get install -y msodbcsql18

RUN pip install --no-cache-dir -r requirements.txt
COPY ./ /fastapi/
EXPOSE 80
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]