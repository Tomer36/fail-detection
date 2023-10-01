import logging.handlers
import datetime

# create logger
LOG_FILENAME = 'logs/saluma.log'


logger = logging.getLogger("saluma")
logger.setLevel(logging.DEBUG) # Todo - make logger level dynamic
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")



# create console handler and set level to debug
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)
console_handler.setLevel(logging.DEBUG) #Todo - make this logger level dynamic

# file rotating log
file_handler = logging.handlers.RotatingFileHandler(LOG_FILENAME, maxBytes=10485760, backupCount=5)
file_handler.setFormatter(formatter)


logger.addHandler(console_handler)
logger.addHandler(file_handler)

_log = None
def get_result_logger(run_no=datetime.datetime.now().__str__()):
    global _log
    if _log is None :
        _log = logging.getLogger("saluma_result_logger")
        _log.setLevel(logging.DEBUG)
        file_name = 'data/result_' + run_no
        file_handler = logging.handlers.RotatingFileHandler(file_name, maxBytes=10485760, backupCount=1)
        file_handler.setFormatter(formatter)
        _log.addHandler(file_handler)
    return _log