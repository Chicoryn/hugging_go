TESTS = $(wildcard tests/test*.py)
SRCS = $(wildcard hugging_go/*.py)

test: build-test-image $(TESTS)
	docker run -v $(CURDIR):/app -w /app `docker build -qf Dockerfile.test .` python3 -m unittest $(TESTS)

build-test-image: .dockerignore
	docker build -f Dockerfile.test .

build-image: .dockerignore dist/hugging_go-0.0.0-py3-none-any.whl
	docker build -f Dockerfile .

clean:
	rm -rf model/checkpoint-*

dist/hugging_go-0.0.0-py3-none-any.whl: pyproject.toml setup.cfg $(SRCS)
	python3 -m build --wheel

.dockerignore:
	echo 'data/' > .dockerignore
	echo 'gomill/' > .dockerignore
	ls -dt --ignore='*.json' model/* | grep -v json | tail -n +2 >> .dockerignore

gomill: build-image
	make -C gomill HUGGING_GO_SHA=`docker build -f Dockerfile -q .`

.PHONY: .dockerignore
