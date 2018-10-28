# make SERVICE=worker logs_pod

SERVICE:=web
_CLOUDSDK_COMPUTE_ZONE:=europe-west4-c
_CLOUDSDK_CONTAINER_CLUSTER:=staging

# docker build -t gcr.io/trends-217607/trends:1 $(PWD)
# gcloud docker -- push gcr.io/trends-217607/trends:1
# kompose down
# kompose up
# kubectl delete service web
# kubectl expose deployment web --type="LoadBalancer"

deploy:
	docker-compose up

configure_docker:
	gcloud auth configure-docker

local_ipython_web:
	docker-compose exec web ipython

bash:
	docker-compose exec ${SERVICE} bash

# deploy_local: configure_docker
# 	docker pull gcr.io/trends-217607/trends:1 && docker-compose up

deploy_hard:
	docker-compose stop && docker-compose rm -f && docker-compose up --build

ipython:
	docker-compose exec ${SERVICE} ipython



POD = $(shell kubectl get pods | grep ${SERVICE} | cut -d " " -f1)

logs_pod:
	kubectl logs ${POD}

service_watch:
	kubectl get service ${SERVICE} --watch

pods:
	kubectl get pods

get_deployments:
	kubectl get deployments

gcloud_bash:
	kubectl exec -it ${POD} -c ${SERVICE} bash

gcloud_ipython:
	kubectl exec -it ${POD} -c ${SERVICE} ipython

auth:
	gcloud auth login

set_project: auth
	gcloud config set project $(shell gcloud config get-value core/project)

get_credentials: set_project
	gcloud container clusters \
	    get-credentials ${_CLOUDSDK_CONTAINER_CLUSTER} \
	    --zone ${_CLOUDSDK_COMPUTE_ZONE}

gke:
	gcloud compute instances list

node:
	kubectl get nodes

get_internal_ip:
	kubectl get service ${SERVICE} --watch