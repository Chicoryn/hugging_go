report: build-image
	docker run -it \
		-e HUGGING_GO_SHA=$(HUGGING_GO_SHA) \
		-v /var/run/docker.sock:/var/run/docker.sock \
		-v $(PWD)/gomill:/app -w /app \
		`docker build -q .` \
		ringmaster playoff.ctl.py

build-image:
	docker build .
