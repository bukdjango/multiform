
build:
	docker build --tag=test .

test:
	docker run --rm test python ./runtests.py

install:
	docker run --rm test pip install .

run: build
	docker run -p 8000:8000 --rm -it test python ./manage.py runserver 0.0.0.0:8000

suite: build test install
build-test: build test