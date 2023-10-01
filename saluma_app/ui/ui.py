from abc import ABC, abstractmethod
from .qt.saluma_ui import load_ui as load_qt_ui

class UI(ABC):

    @classmethod
    def create_instance(cls, product):
        for subclass in UI.__subclasses__():
            if product == subclass.product:
                return subclass()


    @abstractmethod
    def load_ui(self, config_file_path):
        pass



class WEB(UI):
    product = 'WEB'

    def load_ui(self, config_file_path):
        print('loading web UI')
        # Todo - create flask web ui


class QT(UI):
    product = 'QT'

    def load_ui(self, config_file_path):
        print('loading QT UI')
        load_qt_ui(config_file_path)


class CLI(UI):
    product = 'CLI'

    def load_ui(self, config_file_path):
        print('cli ui is based on configuration and made for debug')
