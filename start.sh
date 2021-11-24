docker-compose stop
docker-compose rm --force
docker-compose build
docker-compose up -d
docker-compose exec web bash
