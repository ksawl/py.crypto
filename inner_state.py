from tpl.singletonMeta import SingletonMeta
from constant import METHODS_LIST


class InnerState(metaclass=SingletonMeta):
    def __init__(self):
        self.cipher_method = METHODS_LIST[0]
