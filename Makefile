all: build run

build:
	docker build . -t filmsite

run:
	docker run --rm -it -p 80:8000 --name filmsite filmsite

clean:
	docker image prune -f
