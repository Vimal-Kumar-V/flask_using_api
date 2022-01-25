FROM python:3.10

WORKDIR ./

COPY ./main.py ./main.py


COPY ./requirements.txt  /tmp/requirements.txt

RUN pip install -r /tmp/requirements.txt

RUN flask run

EXPOSE 5000


CMD ["python", "main.py"]
