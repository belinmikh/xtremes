from configuration.configs import JsonConfig
from configuration.descriptors import Field


class Config(JsonConfig):
    log_filename = Field(str, default="data/xtremes.log")
    log_level = Field(str, default="INFO")

    redis_host = Field(str, default="localhost")
    redis_port = Field(int, default=6379)
    redis_db = Field(int, default=0)

    file_url = Field(str, default="https://minjust.gov.ru/uploaded/files/exportfsm.csv")
    file_column = Field(str, default="Материал")
    file_encoding = Field(str, default="Windows-1251")
    file_delimiter = Field(str, default=";")
    file_updating_hours = Field(int, default=24)

    keywords_file = Field(str, default="keywords.json")
