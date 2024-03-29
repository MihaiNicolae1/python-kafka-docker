import os
from enum import Enum


class EnvironmentVariables(str, Enum):
    KAFKA_SHIPPING_TOPIC_NAME = 'KAFKA_SHIPPING_TOPIC_NAME'
    KAFKA_FULFILL_TOPIC_NAME = 'KAFKA_FULFILL_TOPIC_NAME'
    KAFKA_SERVER = 'KAFKA_SERVER'
    KAFKA_PORT = 'KAFKA_PORT'

    def get_env(self, variable=None):
        return os.environ.get(self, variable)
