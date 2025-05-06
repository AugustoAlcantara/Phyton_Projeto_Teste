# Etapa 1: Definir a imagem base
FROM python:3.9-slim

# Etapa 2: Definir o diretório de trabalho no contêiner
WORKDIR /app

# Etapa 3: Copiar o arquivo de dependências para o contêiner
COPY requirements.txt .

# Etapa 4: Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Etapa 5: Copiar o código do projeto para o contêiner
COPY . .

# Etapa 6: Expor a porta onde o servidor vai rodar
EXPOSE 8000

# Etapa 7: Comando para rodar o servidor quando o contêiner iniciar
CMD ["uvicorn", "app.server:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
