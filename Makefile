SERVICE:=web

deploy:
	docker build -t gcr.io/trends-217607/trends:1 $(PWD)
	gcloud docker -- push gcr.io/trends-217607/trends:1
	kompose down
	kompose up
	kubectl delete service web
	kubectl expose deployment web --type="LoadBalancer"

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