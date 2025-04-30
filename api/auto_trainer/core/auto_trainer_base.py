from abc import abstractmethod
from auto_trainer.core.singleton import Singleton

# Product
class AutoTrainer(Singleton):
  @abstractmethod
  def config(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def captar(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def treinar_validar_versionar(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def selecionar(self) -> None:
    raise NotImplementedError

  @abstractmethod
  def promover(self) -> None:
    raise NotImplementedError

  def training(self) -> None:
    self.captar()
    self.treinar_validar_versionar()
    self.selecionar()
    self.promover()