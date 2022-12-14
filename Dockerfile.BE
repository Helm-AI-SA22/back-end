FROM python:3.8-slim-buster

RUN apt update
RUN apt install htop

### fix user
RUN useradd -ms /bin/bash backenduser
USER backenduser
WORKDIR /home/backenduser
RUN cd /home/backenduser && mkdir workdir

WORKDIR /home/backenduser/workdir

COPY . .

# set the env variable DEPLOY
ENV DEPLOY=true

RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

# Start the app
CMD [ "python", "-u", "app.py" ]