FROM python:3.7

ENV PYTHONUNBUFFERED=1
RUN mkdir /code
WORKDIR /code
ADD . /code/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
CMD ["python","./manage.py", "runserver",  "0.0.0.0:8000"]

