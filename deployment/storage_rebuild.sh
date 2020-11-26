HOME_DIRECTORY=/home/$(whoami)

docker-compose down

docker rmi storage --force
docker system prune --force

sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"

sudo cp -r ./config "$HOME_DIRECTORY"

cd ..
cd StorageService
docker build -t storage:latest .

docker-compose up -d