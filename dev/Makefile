configure:
	make clean

up:
	docker-compose up -d

start:
	docker-compose start

down:
	docker-compose down

clean:
	docker-compose rm -f

rm-volumes:
	docker volume rm $(docker volume ls -q)

open:
	x-www-browser http://localhost:3000
