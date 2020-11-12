cd ..
cd AuditService
docker build -t audit:latest .

cd ..
cd ProcessingService
docker build -t processing:latest .

cd ..
cd RecieverService
docker build -t reciever:latest .

cd ..
cd StorageService
docker build -t storage:latest .

cd ..
cd deployment
docker-compose up -d