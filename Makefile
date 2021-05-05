image = effprime/basement-bot-api
dev-image = $(image):dev
prod-image = $(image):prod
drun = docker run --rm -v $(shell pwd)/app:/var/api/app -t $(dev-image) python3 -m

make sync:
	python3 -m pipenv sync -d

check-format:
	$(drun) black --check app/
	$(drun) isort --check-only app/

format:
	$(drun) black app/
	$(drun) isort app/

lint:
	$(drun) pylint app/*.py

test:
	$(drun) pytest --disable-warnings

dev:
	docker build -t $(dev-image) -f Dockerfile.dev .

prod:
	docker build -t $(prod-image) -f Dockerfile .

upd:
	docker-compose -f docker-compose.yml -f docker-compose.override.yml up -d

upp:
	docker-compose -f docker-compose.yml up -d

down:
	docker-compose down

reboot:
	make down && make dev && make upd && make logs

restart:
	docker-compose restart

logs:
	docker logs basement_bot_api -f
