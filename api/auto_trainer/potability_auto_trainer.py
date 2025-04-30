
import pandas as pd
import mlflow
from datetime import datetime
from mlflow.tracking.client import MlflowClient
from auto_trainer.core.auto_trainer_base import AutoTrainer
from auto_trainer.core.auto_trainer_factory import AutoTrainerFactory
from auto_trainer.potability_linear_model import PotabilityLinearModel
from sklearn.metrics import mean_squared_error as mse
from sklearn.metrics import mean_absolute_error as mae
from sklearn.metrics import mean_absolute_percentage_error as mape

# Product
class PotabilityAutoTrainer(AutoTrainer):
  def config(self, url, experiment, sample_url, run_name, model_name) -> None:
    mlflow.set_tracking_uri(url)
    mlflow.set_experiment(experiment)

    self.current_time = datetime.now().strftime("%d/%m/%Y - %H:%M:%S")

    self.sample_url = sample_url
    self.run_name = run_name
    self.model_name = model_name
    self.myColumnsX = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
      'Organic_carbon', 'Trihalomethanes', 'Turbidity']
    self.myColumnsY = ['Potability']

  def captar(self) -> None:
    sample_data = pd.read_csv(self.sample_url)
    self.df = sample_data

  def treinar_validar_versionar(self):
    self.metrics_vector = []

    run_name = f'{self.run_name}'

    mlflow.start_run(run_name=run_name)

    run = mlflow.active_run()

    run_id = run.info.run_id

    linearModel = PotabilityLinearModel()
    linearModel.pre_processar(self.df)
    self.df = linearModel.df
    self.X_train = linearModel.X_train
    self.X_test = linearModel.X_test
    self.y_train = linearModel.y_train
    self.y_test = linearModel.y_test
    linearModel.fit()

    predict = linearModel.predict(self.X_test)
    metricas = {
      'MSE': mse(predict, self.y_test),
      'MAE': mae(predict, self.y_test),
      'MAPE': mape(predict, self.y_test)
    }

    mlflow.set_tag("data", self.current_time)
    mlflow.log_metrics(metricas)
    mlflow.log_artifact(self.sample_url)

    mlflow.sklearn.log_model(linearModel.model, self.model_name)

    mlflow.end_run()

    print('*********************************')
    print(metricas)
    print('*********************************')
    self.metrics_vector.append([run_name, run_id, metricas, metricas['MAPE'], self.model_name])

  def selecionar(self) -> None:
    df = pd.DataFrame(self.metrics_vector, columns = ["run_name", "rund_id", "metricas", "mape", "model_name"])
    self.df = df.sort_values(by=['mape'], ascending=False)

  def promover(self) -> None:
    # The default path where the MLflow autologging function stores the model
    run_id = self.df["rund_id"].loc[0]
    artifact_path = self.df["model_name"].loc[0]
    model_uri = f"runs:/{run_id}/{artifact_path}"

    model_details = mlflow.register_model(model_uri=model_uri, name=self.model_name)

    client = MlflowClient()

    # Adicionar descrição ao modelo
    client.update_registered_model(
      name=model_details.name,
      description="Este modelo possui o intuito de identificar água potável dadas as características"
    )

    # Adicionar descrição à versão
    client.update_model_version(
      name=model_details.name,
      version=model_details.version,
      description="Esta é a primeira versão do modelo capaz de identificar água potável dadas as características"
    )

    print('**********************')
    print('Promote')
    print('**********************')
    client.transition_model_version_stage(
      name=model_details.name,
      version=model_details.version,
      stage='Production',
    )

class PotabilityAutoTrainerFactory(AutoTrainerFactory):
  def createAutoTrainer(self) -> AutoTrainer:
    return PotabilityAutoTrainer()