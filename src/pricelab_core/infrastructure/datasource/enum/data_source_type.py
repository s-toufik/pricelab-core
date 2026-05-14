from enum import Enum


class DataSourceType(Enum):
    api = "api"
    database = "database"
    cache = "cache"
    file = "file"
