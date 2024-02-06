ifndef workers
override workers = 3
endif

run-scheduler:
	make down && docker compose up redis scheduler

del-redis:
	rm redis_data/dump.rdb

down:
	rm examples/celerybeat-schedule || true && docker compose down

build:
	docker compose build

run:
	make down && docker compose up

clean-run:
	docker compose down --volumes && make run

build-and-run:
	make build && make run

run-scale:
	make down && docker compose up --scale worker='$(workers)'

build-and-run-scale:
	make down && make build && make run-scale
