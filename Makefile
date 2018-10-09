SERVICE:=web
_CLOUDSDK_COMPUTE_ZONE:=europe-west4-c
_CLOUDSDK_CONTAINER_CLUSTER:=cluster-1
PROJECT:=trends-217607

deploy:
	docker build -t gcr.io/trends-217607/trends:1 $(PWD)
	gcloud docker -- push gcr.io/trends-217607/trends:1
	kompose down
	kompose up
	# kubectl delete service web
	# kubectl expose deployment web --type="LoadBalancer"

deploy_local:
	docker-compose up

deploy_local_reset:
	docker-compose up --build

POD = $(shell kubectl get pods | grep ${SERVICE} | cut -d " " -f1)

logs_pod:
	kubectl logs ${POD}

service_watch:
	kubectl get service ${SERVICE} --watch

pods:
	kubectl get pods

get_deployments:
	kubectl get deployments

attach:
	kubectl attach ${POD}

auth:
	gcloud auth login

set_project: auth
	gcloud config set project $(shell gcloud config get-value core/project)

get_credentials: set_project
	gcloud container clusters \
	    get-credentials ${_CLOUDSDK_CONTAINER_CLUSTER} \
	    --zone ${_CLOUDSDK_COMPUTE_ZONE}
