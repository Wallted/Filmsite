FROM python:3.6

RUN apt-get update 


WORKDIR /usr/src/app

COPY filmsite/requirements.txt ./
RUN pip install -r requirements.txt

COPY filmsite/ filmsite
COPY data/my-data.json my-data.json
COPY data/my-media/ filmsite/media


WORKDIR /usr/src/app/filmsite

RUN python3 manage.py migrate
# RUN python3 manage.py app_init
RUN python3 manage.py load_mydata


EXPOSE 8000
ENTRYPOINT [ "python3", "manage.py", "runserver", "0.0.0.0:8000" ]
