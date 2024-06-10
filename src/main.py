from tg_api.bot import create_bot
from settings import settings
from utils.logging_conf import logger


if __name__ == '__main__':
    bot = create_bot(settings.bot.token)
    bot.polling(non_stop=True, interval=1, restart_on_change=True, path_to_watch='tg_api/', skip_pending=True)
    logger.info("Bot finished!")