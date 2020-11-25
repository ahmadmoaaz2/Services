HOME_DIRECTORY=/home/$(whoami)
sudo mkdir -p "$HOME_DIRECTORY/config"
sudo mkdir -p "$HOME_DIRECTORY/logs"
sudo mkdir -p "$HOME_DIRECTORY/nginx"

sudo cp -r ./config "$HOME_DIRECTORY"
sudo cp -r ./nginx "$HOME_DIRECTORY"

docker-compose up -d