import logging
import os

import dotenv
from pydantic import SecretStr, Field
from pydantic_settings import BaseSettings

dotenv.load_dotenv('.env')
dotenv.load_dotenv('.env-endpoints')


class BotSettings(BaseSettings):
    token: SecretStr = SecretStr(os.getenv('BOT_TOKEN'))


class ApiSettings(BaseSettings):
    api_host: SecretStr = SecretStr(os.getenv('API_HOST'))
    api_key: SecretStr = SecretStr(os.getenv('API_KEY'))


class UrlSetting(BaseSettings):
    hostname: str = Field(os.getenv("HOSTNAME"))
    search: str = Field(os.getenv("SEARCH"))
    overview: str = Field(os.getenv("OVERVIEW"))


class Settings(BaseSettings):
    bot: BotSettings = BotSettings()
    api: ApiSettings = ApiSettings()
    url: UrlSetting = UrlSetting()
    logger_name: str = Field(os.getenv("LOG_FILENAME"))

    log_handler_start_message_format: str = (
                                "Started handler: %s;\n INFO ABOUT:\n"
                                "\tchat_id: %s;\n"
                                "\ttext: %s;\n"
                                )

    log_handler_finish_message_format: str = (
                                "Finished handler: %s;\n INFO ABOUT:\n"
                                "\tchat_id: %s;\n"
                                "\ttext: %s;\n"
                                )

    log_handler_error_message_format: str = (
                                        "Failed handler: %s;\nINFO ABOUT:\n"
                                        "\tchat_id: %s;\n"
                                        "\ttext: %s;\n"
                                        "\terror: %s\n"
                                        "\ttraceback: %s"
                                        )

settings = Settings()
logging.basicConfig(
    filename=settings.logger_name,
    filemode='a',
    level=logging.INFO,
    format="[%(asctime)s] %(name)s:%(funcName)s:%(threadName)s:%(levelname)s | %(message)s",
    encoding='utf-8'
)

if __name__ == '__main__':
    print(settings)
    logging.debug('Helelo!')
    logging.info('awdafafsaw!')
    logging.warning('awdsafdasdfafafsaw!')
    logging.critical('%d dada %f', 34, 14.2)

