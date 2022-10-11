FROM python:latest

RUN apt-get update
RUN pip install psycopg2
RUN pip install requests

WORKDIR /home/ubuntu/

COPY config.json /home/ubuntu/config.json
COPY parser.py /home/ubuntu/parser.py

CMD ["python3", "/home/ubuntu/parser.py"]