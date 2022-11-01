.PHONY: help init build destroy create-environment shell exec 

all: help

PROJECT_NAME=HELM-Back-End
DOCKERFILE_NAME=Dockerfile.BE.dev
CONTAINER_NAME=helmbe
IMAGE_NAME=be-container
WORKING_DIR_MOUNT=/home/backenduser/workdir

CN="\\033[0m"
CR="\\033[91m"
CG="\\033[92m"
CY="\\033[93m"
CB="\\033[94m"
CT="\\033[37m"
TB="\\033[1m"

help:
	@echo ""
	@echo "============ ${TB}${CB}Project: ${PROJECT_NAME}${CN}"
	@echo ""
	@echo "  ${CY}make init${CN}					prepare the container ${CR}${CONTAINER_NAME}${CN} with ${CY}build${CN}, ${CY}create-environment${CN} and ${CY}install${CN}"
	@echo "  ${CY}make build${CN}					build docker image, and run container ${CR}${CONTAINER_NAME}${CN}"
	@echo "  ${CY}make destroy${CN}					stop and remove running container ${CR}${CONTAINER_NAME}${CN}"
	@echo "  ${CY}make create-environment${CN}			create virtualenv with container's python, see ${CG}.env${CN}"
	@echo "  ${CY}make install${CN}					install in the virtualenv the dependencies in ${CT}requirements.txt${CN}"
	@echo "  ${CY}make shell${CN}					open shell in ${CR}${CONTAINER_NAME}${CN}"
	@echo "  ${CY}make exec${CN}					start Flask application in the container"
	@echo ""
	@echo "============"
	@echo ""
	@echo "Hi! if it is your first time dealing with ${CR}${CONTAINER_NAME}${CN} you should do an ${CY}init${CN}, have a nice code."

init: build create-environment install

build:
	@echo "============ ${TB}${CB}Building and start${CN} ${CR}${CONTAINER_NAME}${CN} ..."
	@docker build -f ${DOCKERFILE_NAME} -t ${IMAGE_NAME} .
	@docker run -itd --name ${CONTAINER_NAME} -v ${CURDIR}/:${WORKING_DIR_MOUNT} -p 5000:5000 ${IMAGE_NAME} bash -c "/bin/sleep infinity"
	@echo "============ Done!"

destroy:
	@echo "============ ${TB}${CB}Stopping and removing${CN} ${CR}${CONTAINER_NAME}${CN} ..."
	@docker stop ${CONTAINER_NAME}
	@docker rm -v ${CONTAINER_NAME}
	@echo "============ Done!"

create-environment:
	@echo "============ ${TB}${CB}creating virtualenv${CN} ..."
	@docker exec ${CONTAINER_NAME} bash -c "python -m venv .env"
	@docker exec ${CONTAINER_NAME} bash -c "source .env/bin/activate; pip install --upgrade pip"
	@echo "============ Done!	see ${CG}.env${CN}"

install:
	@echo "============ ${TB}${CB}Installing the requirements.txt${CN} ..."
	@docker exec ${CONTAINER_NAME} bash -c "source .env/bin/activate; pip install -r requirements.txt"
	@echo "============ Done!"

shell:
	@echo "============ ${TB}${CB}Starting shell${CN} ..."
	@docker exec -it ${CONTAINER_NAME} bash

exec:
	@echo "============ ${TB}${CB}Starting Flask app${CN} ..."
	@docker exec -it ${CONTAINER_NAME} bash -c "source .env/bin/activate; python app.py"