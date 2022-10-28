FROM python:3.8-slim-buster

### fix user
RUN useradd -ms /bin/bash backenduser
USER backenduser
WORKDIR /home/backenduser
RUN cd /home/backenduser && mkdir workdir

WORKDIR /home/backenduser/workdir

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt