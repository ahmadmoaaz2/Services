HOME_DIRECTORY=/home/$(whoami)

docker-compose down

docker rmi react --force
docker system prune --force

sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"

sudo cp -r ./config "$HOME_DIRECTORY"

cd ..
cd ui
docker build -t react:latest .

docker-compose up -d