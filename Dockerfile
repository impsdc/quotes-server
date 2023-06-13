# pull official base image
FROM python:3.8

RUN mkdir api
# set work directory
WORKDIR /api

# Allow statements and log messages to immediately appear in the Knative logs
ENV PYTHONUNBUFFERED True

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt /api/requirements.txt
RUN pip install -r requirements.txt

# copy project
COPY ./app /api

CMD gunicorn -w 2 -b 0.0.0.0:5000 wsgi:app