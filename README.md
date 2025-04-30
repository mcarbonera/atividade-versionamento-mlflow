# Projeto de versionamento de modelos em python.

Atividade prática da disciplina de Ciclo de Vida de Modelo, da especialização de Machine Learning in Production, ofertada pela UFSCAR.

O modelo a ser treinado nessa atividade é para classificação de água potável (https://www.kaggle.com/datasets/adityakadiwal/water-potability/data). O python notebook analise_agua.ipynb contém a etapa de análise descritiva, exploratória, engenharia de recursos e seleção de modelos.

O projeto contém um arquivo docker-compose.yml com as configurações dos seguintes serviços: servidor Mlflow para versionamento de modelos, a API em Flask que possui endpoints para realizar o treinamento, buscar modelo e excluir.

O Mlflow utiliza os bancos de dados PostgreSql e Minio. O MongoDB é utilizado para armazenar os dados de água potável.

## Rodar o projeto:

- docker compose up

## Configuração 

- No Mongo Express, no endereço localhost:8081, fazer login com usuário e senha "mexpress" (definido no docker-compose).
- Criar database com o nome de "water_data".
- Dentro deste database, criar a collection "training_data".
- Inserir os dados com o comando "python3 insert_data.py".
- Acessar o Minio (localhost:9001), fazer login com usuário "minio" e senha "minio123".
- Criar um bucket com nome "mlflow".
- Na sidebar, acessar "Access Keys".
- Criar uma chave de acesso (Access Key e Secret Key).
- Copiar estes valores para o docker-compose.yml, no serviço "tracking_server".
- Para a alteração surtir efeito, parar os containers utilizando "docker compose down", seguido de "docker compose up".
- Após fazer as requisições de treinamento, para ver os modelos salvos, acessar o Mlflow (localhost:5001)

## Inserir dados

- O script insert_data.py foi utilizado para a ingestão dos dados no mongoDB.

## Treinar modelo e salvar no Mlflow:

- GET localhost:5000/train_and_promote
- Parametros de URL (request param):

```
db = water_data
collection=training_data
experiment=1
run_name=1
model_name=linearModel
```

## Fazer previsão sobre o modelo em produção:

- GET http://localhost:5000/model?model_name=linearModel

# Excluir modelo:

- GET http://localhost:5000/delete?model_name=linearModel&version=1
