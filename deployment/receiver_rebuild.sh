HOME_DIRECTORY=/home/$(whoami)

docker-compose down

docker rmi receiver --force
docker system prune --force

sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"

sudo cp -r ./config "$HOME_DIRECTORY"

cd ..
cd ReceiverService
docker build -t receiver:latest .

docker-compose up -d