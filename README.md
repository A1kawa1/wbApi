# wbApi

docker build -t a1kawa/wb_api:latest .  
docker push a1kawa/wb_api:latest

docker run -d --name wb_api -p 8085:8085 a1kawa/wb_api:latest