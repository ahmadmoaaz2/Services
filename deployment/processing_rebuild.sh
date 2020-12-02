HOME_DIRECTORY=/home/$(whoami)

docker-compose down

docker rmi processing --force
docker system prune --force

sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"

sudo cp -r ./config "$HOME_DIRECTORY"

cd ..
cd ProcessingService
docker build -t processing:latest .

cd ..
cd deployment

docker-compose up -d