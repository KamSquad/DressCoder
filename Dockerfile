# pull official base image
FROM python:3.10.0b1-buster
# set work directory
WORKDIR /usr/src/app
# set environment variables
# do not write byte code
ENV PYTHONDONTWRITEBYTECODE 1
# buffer python output
ENV PYTHONUNBUFFERED 1
# copy project
RUN git clone https://github.com/KamSquad/DressCoder.git .
# COPY requirements.txt .
RUN pip install -r ./requirements.txt
# set env
# COPY .env .