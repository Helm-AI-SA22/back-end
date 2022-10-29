.PHONY : build shell exec

all: build create-environment install

build:
	docker build -f Dockerfile.BE.dev -t be-container .
	docker run -itd --name helmbe -v ${CURDIR}/:/home/backenduser/workdir -p 5000:5000 be-container bash -c "/bin/sleep infinity"

destroy:
	docker stop helmbe
	docker rm -v helmbe

create-environment:
	docker exec helmbe bash -c "python -m venv .env"
	docker exec helmbe bash -c "source .env/bin/activate; pip install --upgrade pip"

install:
	docker exec helmbe bash -c "source .env/bin/activate; pip install -r requirements.txt"

shell:
	docker exec -it helmbe bash

exec:
	docker exec -it helmbe bash -c "source .env/bin/activate; python app.py"