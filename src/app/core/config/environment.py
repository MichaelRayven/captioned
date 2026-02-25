from enum import Enum


class Environment(Enum):
    local = 'local'
    test = 'test'
    production = 'deploy'
