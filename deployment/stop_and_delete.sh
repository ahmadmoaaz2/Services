docker-compose down

docker rmi react --force
docker rmi reciever --force
docker rmi audit --force
docker rmi processing --force
docker rmi storage --force
docker system prune