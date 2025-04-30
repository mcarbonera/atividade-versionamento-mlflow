from flask import Flask
from flask import request
import mlflow
import pandas as pd
import os
from auto_trainer.storage_data import StorageData
from auto_trainer.potability_auto_trainer import PotabilityAutoTrainerFactory
from auto_trainer.potability_linear_model import PotabilityLinearModel
from mlflow.tracking.client import MlflowClient
from flask_cors import CORS
import json

mlFlowUrl = 'http://mlflow_server:5000/'

app = Flask(__name__)
CORS(app);

def get_model(model_name):
  try:
    mlflow.set_tracking_uri(mlFlowUrl)

    model_production_uri = "models:/{model_name}/Production".format(model_name=model_name)

    pure_model = mlflow.pyfunc.load_model(model_uri=model_production_uri)
    model_production = PotabilityLinearModel().init_from_mlflow(pure_model)

    run_id = pure_model._model_meta.run_id

    local_path = mlflow.artifacts.download_artifacts(run_id= run_id,
                                                     artifact_path = "water_data_ok.csv",
                                                     dst_path=os.getcwd())

    sample_data = pd.read_csv(local_path)
    model_production.pre_processar(sample_data)

    return model_production.predict(model_production.X_test)

  except Exception as e:
    print(e)
    raise

def train_model(db, collection, experiment, run_name, model_name):
  try:
    storage_data = StorageData()
    client = storage_data.connection("mongo", "27017", "root", "password")
    sample_data = storage_data.get_all_water_data(client, db, collection)

    sample_url = os.getcwd()+"/water_data_ok.csv"
    sample_data.to_csv(sample_url)

    # Auto trainer
    potability_auto_trainer_factory = PotabilityAutoTrainerFactory()
    potability_auto_trainer = potability_auto_trainer_factory.createAutoTrainer()

    potability_auto_trainer.config(
      url = mlFlowUrl,
      experiment = experiment,
      sample_url = sample_url,
      run_name = run_name,
      model_name = model_name,
    )

    potability_auto_trainer.training()

    return "Modelo treinado e promovido com sucesso!"

  except Exception:
    raise

def delete_model(model_name, version):
  try:
    mlflow.set_tracking_uri(mlFlowUrl)

    client = MlflowClient()

    client.delete_model_version(
      name=model_name,
      version=version,
    )

    return "Modelo excluído com sucesso!"

  except Exception:
    raise

@app.route('/model', methods=['GET'])
def index_model():
  response = "Invalid params!"

  if request.method == 'GET':
    model_name = request.args.get("model_name")
    if model_name:
      try:
        response = {'response': get_model(model_name).tolist()}
        response = json.dumps(response)
      except Exception as e:
        print(e)
        response = 'Not Found'
        raise
        return response

  return response

@app.route('/delete', methods=['GET'])
def index_delete():
  response = "Invalid params!"
  if request.method == 'GET':
    model_name = request.args.get("model_name")
    version = request.args.get("version")

    if model_name and version:
      try:
        response = delete_model(
          model_name,
          version
        )
      except:
        response = 'Not Found'
        return response

  return response

@app.route('/train_and_promote', methods=['GET'])
def index_train_and_promote():
  response = "Invalid response!"

  if request.method == 'GET':
    db = request.args.get("db")
    collection = request.args.get("collection")
    experiment = request.args.get("experiment")
    run_name = request.args.get("run_name")
    model_name = request.args.get("model_name")

    if db and collection and experiment and run_name and model_name:
      response = train_model(
        db,
        collection,
        experiment,
        run_name,
        model_name
      )
  return response

if __name__ == "__main__":
  app.run(host='0.0.0.0',port=5000, debug=False)