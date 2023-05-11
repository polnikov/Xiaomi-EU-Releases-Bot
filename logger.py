import logging


log_format = '%(asctime)s %(levelname)s [%(lineno)d] %(filename)s %(message)s'
logging.basicConfig(
    handlers=[logging.FileHandler(filename='bot.log', encoding='utf-8', mode='a+')],
    format=log_format,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

logger = logging.getLogger(__name__)
