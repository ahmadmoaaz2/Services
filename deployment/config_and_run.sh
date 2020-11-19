HOME_DIRECTORY=/home/$(whoami)
mkdir -p "$HOME_DIRECTORY/config"
mkdir -p "$HOME_DIRECTORY/logs"

cp -r ./config "$HOME_DIRECTORY"

docker-compose up -d