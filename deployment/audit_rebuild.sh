HOME_DIRECTORY=/home/$(whoami)

docker-compose down

docker rmi audit --force
docker system prune --force

sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"

sudo cp -r ./config "$HOME_DIRECTORY"

cd ..
cd AuditService
docker build -t audit:latest .

cd ..
cd deployment

docker-compose up -d


