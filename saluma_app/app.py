import traceback
import time
import sys
from data_stream import DataStream
from ui.ui import UI
from __init__ import config, reload_config, write_config, config_file_path
from utils.logger import logger



if __name__ == '__main__':
    if config.has_section('GLOBAL'):
        if config['GLOBAL'].get('datasource') == None or config['GLOBAL'].get('datasource') == '':
            logger.error('Please define config file datasource name (from GLOBAL section): ' + str([subclass.product for subclass in DataStream.__subclasses__()]))
            logger.error('USING DEFAULT - PLC')
            config.set('GLOBAL', 'datasource', 'PLC')
        if config['GLOBAL'].get('uisource') == None or config['GLOBAL'].get('uisource') == '':
            logger.error('Please define config file uisource name (from GLOBAL section): ' + str([subclass.product for subclass in UI.__subclasses__()]))
            logger.error('USING DEFAULT - QT')
            config.set('GLOBAL', 'datasource', 'PLC')



    data_stream = DataStream.create_instance(config['GLOBAL'].get('datasource'))

    ## Todo - uncomment these lines in order to have UI .
    # ui = UI.create_instance(config['GLOBAL'].get('uisource'))
    # ui.load_ui(config_file_path)

    try:
        data_stream.train_data(save_training=True)

        for i in range(sys.maxsize):
            logger.info("Test iteration : " + str(i))
            data_stream.test_data(save_testing=True)
            time.sleep(config['PLC_CONFIG'].getfloat('test_intervals'))
        data_stream.destructor()
    except Exception as e:
        logger.error(e)
        logger.error(traceback.format_exc())






