from sklearn import linear_model;
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import MinMaxScaler
from sklearn.base import BaseEstimator, ClassifierMixin
from sklearn.model_selection import train_test_split
import pandas as pd

# linear_model.LogisticRegression
class PotabilityLinearModel(BaseEstimator, ClassifierMixin):
  def __init__(self, penalty=None, max_iter=1000):
    self.penalty = penalty
    self.max_iter = max_iter
    self.model = linear_model.LogisticRegression(penalty=self.penalty, max_iter=self.max_iter)

  def init_from_mlflow(self, model):
    del self.model
    self.model = model
    return self

  def pre_processar(self, df):
    self.df = df
    self.tratarDadosNulos(self.df)
    self.transformColumns(self.df)
    self.df = df
    return self.df

  def tratarDadosNulos(self, df):
    medianaPh = df['ph'].median()
    medianaSulfate = df['Sulfate'].median()
    medianaTrihalomethanes = df['Trihalomethanes'].median()
    self.df['ph'].fillna(medianaPh, inplace = True)
    self.df['Sulfate'].fillna(medianaSulfate, inplace = True)
    self.df['Trihalomethanes'].fillna(medianaTrihalomethanes, inplace = True)

  def transformColumns(self, df):
    df_train, df_test = train_test_split(df, test_size=1/10, random_state=0)
    myCols = ['ph', 'Hardness', 'Solids', 'Chloramines', 'Sulfate', 'Conductivity',
      'Organic_carbon', 'Trihalomethanes', 'Turbidity']
    transformer = ColumnTransformer([
      ('selector', MinMaxScaler(), myCols)
    ])
    X_train = transformer.fit_transform(df_train)
    features = transformer.get_feature_names_out()
    X_train = pd.DataFrame(X_train, columns=features)
    X_test = pd.DataFrame(transformer.transform(df_test), columns=features)

    y_train = df_train['Potability']
    y_test = df_test['Potability']

    self.X_train = X_train
    self.X_test = X_test
    self.y_train = y_train
    self.y_test = y_test

  def fit(self):
    self.model.fit(X = self.X_train, y = self.y_train)

  def predict(self, df):
    return self.model.predict(df)