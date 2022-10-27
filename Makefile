.PHONY : build shell exec

all: build

build:
	docker build -f Dockerfile.BE -t be-container .

shell:
	docker run -it -v ${CURDIR}/src/:/home/backenduser/src -p 5000:5000 be-container bash

exec:
	docker run -it -v ${CURDIR}/src/:/home/backenduser/src -p 5000:5000 be-container python app.py
