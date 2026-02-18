import os
from enum import Enum


class Environment(str, Enum):
    DEV = "dev"
    STAGE = "stage"
    PROD = "prod"


# Read from environment variable
APP_ENV = Environment(os.getenv("APP_ENV", "dev"))

IS_DEV = APP_ENV == Environment.DEV
IS_STAGE = APP_ENV == Environment.STAGE
IS_PROD = APP_ENV == Environment.PROD
