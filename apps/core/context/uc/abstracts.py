from abc import ABC, abstractmethod


class AbstractUC(ABC):
    @abstractmethod
    def execute(self):
        pass


class AbstractModelUC(AbstractUC):
    @abstractmethod
    def __init__(self):
        pass
