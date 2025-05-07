## WebSocket Server com FastAPI
Servidor WebSocket usando Python, FastAPI e SQLite com suporte a execução via Docker.
Devido o tempo curto(visto que atualmente estou alocado em um grande projeto), e não foi necessariamente proibido usar
um framework para otimizar o tempo, decidi usar o FastAPI, pois é um framework muito popular e fácil de usar.

Utilozo também o "Trae ai", uma ferramentas similar ao "VsCode" e "Cursor" com IA avançada imbutida 
que presta assistência avançada de codificação. 

## Funcionalidades

- Conexão com múltiplos clientes via WebSocket.
- Envio automático da data/hora atual a cada segundo.
- Cálculo do Fibonacci sob demanda por comando via WebSocket.
- Registro e atualização de usuários conectados no banco de dados SQLite.
- Execução simples com Docker.

## Link do repositório
    git clone https://github.com/AugustoAlcantara/Phyton_Projeto_Teste.git\

## ⚙️ Como rodar o projeto (SEM Docker)

Requer Python 3.9+ instalado.

1. **Clone o repositório informado:**
   cd Phyton_Projeto_Teste

2. **Instale as dependências:**
   pip install -r requirements.txt

3. **Rode o servidor:**
   uvicorn app.main:app --reload


## 🐳 Como rodar com Docker

após clonar o repositório, execute o seguinte comando no terminal na pasta do projeto:

1. **Criação da imagem:**	
docker build -t websocket-fastapi-app .

2. **Executar o container:**
docker run -p 8000:8000 websocket-fastapi-app

3. **(Opcional) Usar Docker Compose**
Apenas para fins de demonstração e não sendo necessário, pois o projeto usa o SQLite,
você pode usar `docker-compose` para facilitar o processo:

docker-compose up --build

## Comandos úteis com Docker
```bash
### Listar containers:
docker ps -a
### Parar e remover todos os containers:
docker stop $(docker ps -a -q)
docker rm $(docker ps -a -q)
### Remover imagem:
docker rmi websocket-fastapi-app
### Verificar imagens:
docker images
### Parar/remover containers de uma imagem específica:
docker ps --filter ancestor=websocket-fastapi-app -q | ForEach-Object { docker stop $_; docker rm $_ }
### Remover tudo com Docker Compose:
docker-compose down --rmi all -v
```
