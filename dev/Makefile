configure:
	make clean

up:
	COMPOSE_PROJECT_NAME=unireport docker-compose up -d

start:
	COMPOSE_PROJECT_NAME=unireport docker-compose start

down:
	COMPOSE_PROJECT_NAME=unireport docker-compose down

clean:
	COMPOSE_PROJECT_NAME=unireport docker-compose rm -f

rm-volumes:
	COMPOSE_PROJECT_NAME=unireport docker volume rm $(docker volume ls -q)

open:
	x-www-browser http://localhost:3000
