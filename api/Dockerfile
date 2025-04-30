# Base image
# Atenção a imagem base deve ser a mesma da que vc versionou o modelo
FROM python:3.11.4-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY . .

EXPOSE 5000

CMD [ "flask", "run", "--host=0.0.0.0" ]
#CMD ["python3", "app.py"]

#----------INSTRUCTIONS----------

# buildar a imagem
#docker build -t api .

# executar o container com os containers visualizando a rede da maquina
#docker run -d --name api_container --network host api

# acessar o container
#docker exec -i -t api_container bash

# finalizar a execucao do container
#docker kill api_container

# excluir os containers finalizados
#docker rm $(docker ps -a -q)