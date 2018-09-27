deploy:
	export GOOGLE_APPLICATION_CREDENTIALS=$(PWD)/credentials.json
	# gcloud docker -- push gcr.io/trends-217607/trends:1
	kompose down
	kompose up

deploy_local:
	docker-compose up

deploy_local_reset:
	docker-compose up --build

FLOWER_SERVICE = $(shell kubectl get pods | grep flower | cut -d " " -f1)

logs_flower:
	kubectl logs $(FLOWER_SERVICE)
