import sys
import os
import time
import copy
import socket
import pickle
import traceback
import datetime


from abc import ABC, abstractmethod
import pymodbus
from pymodbus.client.sync import ModbusTcpClient as ModbusClient
import pandas as pd
import zmq

from __init__ import config, reload_config, write_config
from utils.const import HealthGrade
from utils.logger import logger, get_result_logger


logger.info("Connecting to math_engine…")
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:5555")
run_no = datetime.datetime.now().__str__()


class DataStream(ABC):

    @classmethod
    def create_instance(cls, product):
        for subclass in DataStream.__subclasses__():
            if product == subclass.product:
                logger.info(subclass.info)
                return subclass()


    @abstractmethod
    def read_data(self):
        pass

    @abstractmethod
    def train_data(self):
        pass

    @abstractmethod
    def test_data(self):
        pass

    @abstractmethod
    def destructor(self):
        pass


    def convert_received_object(self, buffer_obj):
        obj = pickle.loads(buffer_obj)
        status = obj.get('status')
        method = obj.get('method')
        result = obj.get('result')
        msg = obj.get('msg')
        return status, method, msg, result

    def send_data(self, method, data, inner_sensors, outer_sensors):
        logger.debug("---------------------------------------------------------------")
        to_send_data = {"method": method, "dataframe": data, "inner_sensors" : inner_sensors, "outer_sensors": outer_sensors}
        start = time.time()
        socket.send(pickle.dumps(to_send_data))
        #  Get the reply.
        answer = socket.recv()
        status, method, msg, result = self.convert_received_object(answer)
        end = time.time()
        logger.debug("computation took : %.3f" % (end - start,))
        logger.debug("status : " + str(status))
        logger.debug("method : " + method)
        # print("Result : " + str(result))
        logger.debug("msg    : " + msg)
        logger.debug("---------------------------------------------------------------")
        return status, result

    def pivot_dataframe(self, current_df):
        df = pd.pivot_table(current_df, values='VarValue', index=['TimeString'], columns=['VarName'])
        if '$RT_OFF$' in df.columns:
            df.drop(['$RT_OFF$'], axis=1, inplace=True)
        if df.index.name != 'TimeString':
            df.set_index(['TimeString'], drop=True, inplace=True)
        df.dropna(inplace=True)
        return df

class CSV(DataStream):
    product = 'CSV'
    info = 'You ar using CSV datastream'

    sensors = ['FIT-01', 'FIT-02', 'FIT-03', 'PIT-02', 'PIT-03', 'PIT-05', 'PIT-06']
    role = ['inner', 'outer', 'outer', 'outer', 'outer', 'outer', 'outer']
    data_dir = 'C:\\Oren\\Work\\Promacon\\BeerGordon\\data\\'
    data_dir = "data/"
    plot_dir = 'C:\\Oren\\Work\\Promacon\\BeerGordon\\plot\\'
    plot_dir = 'plot/' + time.time().__str__()
    filedate = [['20190526', 0],
                ['20190531', 0],
                ['20190603', 1],
                ['20190604', 1],
                ['20190605', 1],
                ]  # ['20190608', 1]

    trn_files = 2
    file_sn = 0
    line_sn = 0
    extend_degree = 2  # 1 #
    trn_df = pd.DataFrame()

    inner_sensors = None
    outer_sensors = None

    def __init__(self):
        self.inner_sensors = self.__create_inner_sensors()
        self.outer_sensors = self.__create_outer_sensors()

    def __create_inner_sensors(self):
        return [self.sensors[index] for index, v in enumerate(self.role) if v == 'inner']

    def __create_outer_sensors(self):
        return [self.sensors[index] for index, v in enumerate(self.role) if v == 'outer']

    def read_data(self):
        logger.info('READ DATA from plc ')

    def destructor(self):
        pass

    def train_data(self):
        line_sn = 0
        file_sn = 0
        trn_df = pd.DataFrame()

        for trn_file in self.filedate:
            line_sn = line_sn + 1
            if trn_file[1] == 0:
                continue
            if file_sn >= self.trn_files:
                break
            file_sn = file_sn + 1
            # current_df = pd.DataFrame()
            # read csv from key-value table
            filename = '%sRO_History%s.csv' % (self.data_dir, trn_file[0])
            current_df = pd.read_csv('%s' % filename)


            # the section below is replacing the pivot dataframe
            ##########################################
            # trn_df = pd.pivot_table(current_df, values='VarValue', index=['TimeString'], columns=['VarName'])
            # trn_df = trn_df.append(pivoted_current_df)

            # pivoted_current_df = pd.pivot_table(current_df, values='VarValue', index=['TimeString'], columns=['VarName'])

            # if '$RT_OFF$' in trn_df.columns:
            #     pivoted_current_df.drop(['$RT_OFF$'], axis=1, inplace=True)
            # if pivoted_current_df.index.name != 'TimeString':
            #     pivoted_current_df.set_index(['TimeString'], drop=True, inplace=True)
            # pivoted_current_df.dropna(inplace=True)
            ####################


            pivoted_current_df = self.pivot_dataframe(current_df)
            trn_df = trn_df.append(pivoted_current_df)
        self.send_data("train", trn_df, self.inner_sensors, self.outer_sensors)

    def test_data(self):
        line_sn = 0
        # Reads only the last file ffs
        while line_sn <= len(self.filedate):
            tst_file = self.filedate[line_sn - 1]
            if tst_file[1] == 0:
                line_sn = line_sn + 1
                continue
            break
        # just replace the filename with file from the server named by filedate
        tst_filename = '%sRO_History%s.csv' % (self.data_dir, tst_file[0])
        logger.debug("test filename : %s" % tst_filename)
        raw_tst_df = pd.read_csv('%s' % tst_filename)
        tst_df = self.pivot_dataframe(raw_tst_df)
        # tst_df = pd.pivot_table(raw_tst_df, values='VarValue', index=['TimeString'], columns=['VarName'])
        # if '$RT_OFF$' in tst_df.columns:
        #     tst_df.drop(['$RT_OFF$'], axis=1, inplace=True)
        # if tst_df.index.name != 'TimeString':
        #     tst_df.set_index(['TimeString'], drop=True, inplace=True)
        # tst_df.dropna(inplace=True)

        status, result = self.send_data("test", tst_df, self.inner_sensors, self.outer_sensors)

        for time_string, health_grade in result:  # result is an array made of tuples, [0] = time_string [1] health_grade
            if health_grade != HealthGrade.HG_GOOD:
                raise Exception("Error at: " + time_string)

class PLC(DataStream):
    product = 'PLC'
    info = 'You ar using PLC datastream'

    inner_sensors = None
    outer_sensors = None

    def __init__(self):
        self.modbus_client = None
        self.inner_sensors = self.__create_inner_sensors()
        self.outer_sensors = self.__create_outer_sensors()
        # import pdb;pdb.set_trace()

    # Todo - create these function __create... 
    def __create_inner_sensors(self):
        return [key.upper() for key, v in config.items('REGISTERS') if v.split(',')[1] == 'inner']

    def __create_outer_sensors(self):
        return [key.upper() for key, v in config.items('REGISTERS') if v.split(',')[1] == 'outer']
        # return [self.sensors[index] for index, v in enumerate(self.role) if v == 'outer']

    def _convert_registers_to_dataframe(self, reg, timestamp):
        # logger.info(__name__)

        # logger.info("PT-020 : " + str(reg[8]/10))
        # logger.info("PT-021 : " + str(reg[9]/10))
        # logger.info("PT-022 : " + str(reg[10]/10))
        # logger.info("PT-023 : " + str(reg[11]/10))
        # logger.info("DPT-035 : " + str(reg[12]/10))
        # logger.info("FIT-044 : " + str(reg[13]/10))
        # logger.info("FT-043 : " + str(reg[15]/10))
        # logger.info("AIT-031 : " + str(reg[16]/10))
        # logger.info("AIT-031-T : " + str(reg[17]/10))
        # logger.info("AIT-032 : " + str(reg[18]/10))
        # logger.info("P-008-PV : " + str(reg[22]/10))

        # VarName , TimeString, VarValue, Validity
        raws = []
        for key, value in config.items('REGISTERS'):
            dataframe_raw = [key.upper(),timestamp, reg[int(value.split(',')[0])]/10]
            raws.append(dataframe_raw)

        data_frame = pd.DataFrame(raws, columns=['VarName', 'TimeString', 'VarValue'])
        return data_frame

    def read_data(self):
        try:
            rr = self.__read_data()
            # example : [0, 0, 52, 12, 8, 10, 19, 24, 19, 11, 1, 0, 0, 0, 0, 0, 101, 606, 10188, 124, 37]
            if rr.registers and type(rr.registers) == list:

                modbus_registers = copy.copy(rr.registers)
                # print(modbus_registers )
                # Todo - need to add mandatory fields here such as TimeString
                data_frame = self._convert_registers_to_dataframe(modbus_registers, datetime.datetime.now())
                return data_frame
            else:
                raise Exception(
                    'modbus registers error, check modbus connection params {ip}:{port} return registers value: {rr}'.format(
                        ip=config['PLC_CONFIG'].get('ip'), port=config['PLC_CONFIG'].getint('port'), rr=rr))



        # except AttributeError
        except Exception as ex:
            sys.stdout.write("\n")
            logger.error("Modbus connection failed : " + str(ex))
            raise ex

    def __read_data(self, count=10):
        UNIT = 0x1
        if count == 0:
            raise Exception("couldn't reestablish modbus connection after 10 retries")

        try:
            if (not self.modbus_client or not self.modbus_client.is_socket_open()):
                self.modbus_client = ModbusClient(config['PLC_CONFIG'].get('ip'), config['PLC_CONFIG'].getint('port'))
                self.modbus_client.connect()
            rr = self.modbus_client.read_holding_registers(0, 23, unit=UNIT)
            if type(rr) == pymodbus.exceptions.ModbusIOException:
                logger.error("modbus failure number : {no}, retrying ".format(no=10-count))
                logger.error("273")
                time.sleep(1)
                self.modbus_client = None
                return self.__read_data(count-1)
        except pymodbus.exceptions.ConnectionException as e:
            logger.info(str(e))
            logger.error("modbus failure number : {no}, retrying ".format(no=10 - count))
            logger.error("279")
            time.sleep(5*(10-count+1))
            self.modbus_client = None
            return self.__read_data(count - 1)
        return rr

    def test_data(self, save_testing=True):
        test_pf = self.read_data()
        test_pf = self.pivot_dataframe(test_pf)
        # need to make sure we are adding every sample to a file - debugging_purposes.
        if(save_testing):
            if os.path.exists('data/test_'+ run_no + '.csv'):
                test_pf.to_csv('data/test_'+ run_no + '.csv', mode='a', header=False)
            else:
                test_pf.to_csv('data/test_' + run_no + '.csv', )

        status, result  = self.send_data("test", test_pf, self.inner_sensors, self.outer_sensors)
        # Todo - analyze result.

        for time_string, health_grade in result:  # result is an array made of tuples, [0] = time_string [1] health_grade
            if health_grade != HealthGrade.HG_GOOD:
                get_result_logger(run_no).error('Please check testing data, at : ' + str(time_string) + ' HealthGrade was: ' + str(health_grade))
                get_result_logger(run_no).error('Test frame: \n ' + test_pf.__str__())
                # raise Exception("Error at: " + str(time_string))



    def train_data(self, save_training=False, train_from_memory=False):
        if train_from_memory:
            #Todo - load the object from memory
            pass
        bar_length = 40
        end_val = config['PLC_CONFIG'].getint('train_data_no_samples')
        start_time = time.time()
        training_dataframes = pd.DataFrame()
        logger.info("Gathering {no} samples : ".format(no=end_val))
        for i in range(end_val):
            percent = float(i) / end_val
            hashes = '#' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            training_dataframes = training_dataframes.append(self.read_data())
            sys.stdout.write("\rGathering samples: [{0}] {1}% ({2} seconds passed)".format(hashes + spaces, int(round(percent * 100)), int(time.time()-start_time)))
            sys.stdout.flush()
        sys.stdout.flush() # clear progress bar .
        sys.stdout.write("\n")

        # pivot table.
        training_dataframes = self.pivot_dataframe(training_dataframes)

        if(save_training):
            training_dataframes.to_csv('data/train_'+ run_no + '.csv')
        self.send_data("train", training_dataframes, self.inner_sensors, self.outer_sensors)
        # Todo - save the training data in memory (for future purposes )




    def cli_progress_bar(seld, end_val=config['PLC_CONFIG'].getint('train_data_no_samples'), bar_length=40):

        for i in range(0, end_val):
            percent = float(i) / end_val
            hashes = '#' * int(round(percent * bar_length))
            spaces = ' ' * (bar_length - len(hashes))
            sys.stdout.write("\rGathering samples: [{0}] {1}%".format(hashes + spaces, int(round(percent * 100))))
            sys.stdout.flush()
            time.sleep(0.01)
        sys.stdout.write("\n")

    def destructor(self):

        if self.modbus_client:
            self.modbus_client.close()


