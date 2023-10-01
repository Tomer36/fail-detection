import logging.handlers

# create logger
LOG_FILENAME = 'logs/saluma.log'


logger = logging.getLogger("saluma")
logger.setLevel(logging.DEBUG) # Todo - make logger level dynamic
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")



# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)


# file rotating log
file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
file_handler.setFormatter(formatter)


logger.addHandler(console_handler)
logger.addHandler(file_handler)
