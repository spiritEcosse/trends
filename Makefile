deploy:
	export GOOGLE_APPLICATION_CREDENTIALS=$(PWD)."credentials.json"
	kompose down && kompose up
	