from enum import Enum


# Enumerations (or enums) are available in Python since version 3.4.
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
