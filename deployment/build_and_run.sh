HOME_DIRECTORY=/home/$(whoami)
sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"
sudo mkdir -p "$HOME_DIRECTORY/nginx"

sudo cp -r ./config "$HOME_DIRECTORY"
sudo cp -r ./nginx "$HOME_DIRECTORY"

cd ..
cd AuditService
docker build -t audit:latest .

cd ..
cd ProcessingService
docker build -t processing:latest .

cd ..
cd ReceiverService
docker build -t receiver:latest .

cd ..
cd StorageService
docker build -t storage:latest .

cd ..
cd ui
docker build -t react:latest .

cd ..
cd deployment
docker-compose up -d