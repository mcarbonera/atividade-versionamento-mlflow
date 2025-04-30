from pymongo import MongoClient
import pandas as pd
from auto_trainer.core.singleton import Singleton

class StorageData(Singleton):
  def connection(self, host: str, port: str, user: str, password: str) -> MongoClient:
    try:
      client = MongoClient(f"mongodb://{user}:{password}@{host}:{port}/")
      print("Connection Successful!")
      return client
    except Exception as e:
      print("Connection Error!")
      raise e

  def insert_all_water_data(self, client: MongoClient, df: pd.DataFrame, name_of_db: str,  name_of_collection: str) -> None:
    try:
      db = client[name_of_db]
      db_collection = db[name_of_collection]

      list_df = df.to_dict('records')

      db_collection.insert_many(list_df)

      print("Insertion Successful!")

    except Exception as e:
      print("Insertion Error!")
      raise e

  def get_all_water_data(self, client: MongoClient, db_name: str, collection_name: str) -> pd.DataFrame:
    try:
      db = client[db_name]
      db_collection = db[collection_name]
      df = pd.DataFrame(list(db_collection.find()))

      print("Recovering Successful!")

      return df
    except Exception as e:
      print("Error when recovering!")
      raise e