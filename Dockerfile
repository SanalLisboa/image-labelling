FROM python:3.8

WORKDIR /code/
COPY . /code/

RUN pip install -r requirements.txt
RUN mkdir /static
RUN python manage.py collectstatic
RUN mkdir /var/tmp/image_labelling
