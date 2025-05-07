# WebSocket Server com FastAPI

## Como rodar o projeto

1. Clone o repositório:
   git clone https://github.com/seuusuario/websocket-server.git


2. Instale as dependências:
    pip install -r requirements.txt

3. Rode o servidor:
    uvicorn app.main:app --reload

###########################################
Para rodar com Docker:

1. Construa a imagem:
    docker build -t websocket-fastapi-app .

2. Rode o container:
docker run -p 8000:8000 websocket-fastapi-app

3. Reconstruir a imagem:
    docker-compose up --build

###########################################
Listar todos os containers:
    docker ps -a

3. Parar e remover todos os containers:
    parar todos container
    docker stop $(docker ps -a -q)
    docker rm $(docker ps -a -q)

4. Remover a imagem especifica:
    docker stop + id da imagem
    docker rmi websocket-server
    ou
    docker rm + id da imagem

5. Verificar se a imagem foi removida:
    docker images 

docker ps -a --format "table {{.ID}}\t{{.Image}}\t{{.Names}}\t{{.Status}}"


##########################################

1. Parar e remover todos os containers que usam a imagem:
docker ps --filter ancestor=websocket-fastapi:latest -q | ForEach-Object { docker stop $_; docker rm $_ }

2. Verificar se sobrou algum parado:
    docker ps -a --filter ancestor=websocket-fastapi:latest

        2.1 Se ainda aparecerem containers, remova com:
            docker ps -a --filter ancestor=websocket-fastapi:latest -q | ForEach-Object { docker rm $_ }

3. Remova tudo com docker-compose:
docker-compose down --rmi all -v
