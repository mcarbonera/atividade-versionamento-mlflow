# Script para inicializar o banco de dados de treino
from pymongo import MongoClient
import pandas as pd

def get_client(user, password, host, port):
  client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
  print("Connection Successful!")
  return client

def insert_all_water_data(client: MongoClient, df: pd.DataFrame, name_of_db: str,  name_of_collection: str) -> None:
  try:
    db = client[name_of_db]
    db_collection = db[name_of_collection]
    list_df = df.to_dict('records')
    db_collection.insert_many(list_df)
    print("Insertion Successful!")
  except Exception as e:
    print("Insertion Error!")
    raise e

def insert_data():
  try:
    client = get_client("root", "password", "localhost", "27017")
    df = pd.read_csv('water_potability.csv')
    r, c = df.shape
    insert_all_water_data(client, df, 'water_data', 'training_data')
    print("Dados inseridos: " + str(r))
  except Exception:
    raise

def start():
  insert_data()

if __name__ == '__main__':
  start()