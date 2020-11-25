docker-compose down

docker rmi react --force
docker rmi receiver --force
docker rmi audit --force
docker rmi processing --force
docker rmi storage --force
docker system prune --force