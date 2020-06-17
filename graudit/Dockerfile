FROM python:3

RUN apt-get update && \
    apt-get upgrade -y

RUN pip install -U setuptools

RUN pip install psycopg2 six 

COPY tar2db.py /src/

ENTRYPOINT [ "python", "/src/tar2db.py" ]


