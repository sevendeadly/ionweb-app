.PHONY: install  lint build run clean

install:
	pip install -r requirements.txt


build:
	docker-compose build

run:
	docker-compose up

clean:
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -r {} +