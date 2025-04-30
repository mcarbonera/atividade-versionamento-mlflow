from auto_trainer.core.singleton import Singleton
from abc import abstractmethod
from auto_trainer.core.auto_trainer_base import AutoTrainer

class AutoTrainerFactory(Singleton):
  @abstractmethod
  def createAutoTrainer(self) -> AutoTrainer:
    raise NotImplementedError