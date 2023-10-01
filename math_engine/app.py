import sys
import time
import pickle
import zmq
import traceback
import pandas as pd
from utils.const import HealthGrade
from utils.logger import logger

from modeling import MultiDimensionalModeling


sensors = ['FIT-01', 'FIT-02', 'FIT-03', 'PIT-02', 'PIT-03', 'PIT-05', 'PIT-06']
role = ['explained', 'explanatory', 'explanatory', 'explanatory', 'explanatory', 'explanatory', 'explanatory']
data_dir = 'C:\\Oren\\Work\\Promacon\\BeerGordon\\data\\'
data_dir = "data/"
plot_dir = 'C:\\Oren\\Work\\Promacon\\BeerGordon\\plot\\'
plot_dir = 'plot/' + time.time().__str__()
filedate = [['20190526', 0],
    ['20190531', 0],
    ['20190603', 1],
    ['20190604', 1],
    ['20190605', 1],
    ['20190608', 1]]

trn_files = 2
file_sn = 0
line_sn = 0
extend_degree = 2#1 #
trn_df = pd.DataFrame()

# ZMQ server connection.
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind("tcp://*:5555")

# for trn_file in filedate:
#     line_sn = line_sn +1
#     if trn_file[1] == 0:
#         continue
#     if file_sn >= trn_files:
#         break
#     file_sn = file_sn + 1
#     current_df = pd.DataFrame()
#     # read csv from key-value table
#     filename = '%sRO_History%s.csv' % (data_dir, trn_file[0])
#     current_df = pd.read_csv('%s' % filename)
#
#     pivoted_current_df = pd.pivot_table(current_df, values='VarValue', index=['TimeString'], columns=['VarName'])
#     trn_df = trn_df.append(pivoted_current_df)
# if '$RT_OFF$' in trn_df.columns:
#     trn_df.drop(['$RT_OFF$'], axis = 1, inplace = True)
# if trn_df.index.name != 'TimeString':
#     trn_df.set_index(['TimeString'], drop = True, inplace = True)
# trn_df.dropna(inplace = True)
#
# explained_names = [sensors[index] for index, v in enumerate(role) if v == 'explained']
# explanatory_names = [sensors[index] for index, v in enumerate(role) if v == 'explanatory']
# X_trn= trn_df[explanatory_names]
# y_trn = trn_df[explained_names]
# md_obj = MultiDimensionalModeling()
# trn_obj = md_obj.training_handler(X_trn, y_trn, extend_degree)
# md_obj.plot_model_phase(trn_obj, trn_obj, 'BeerGordon', explained_names, explanatory_names, extend_degree, 'training', plot_dir)

#
#
#
# # read data for testing
# tst_df = pd.DataFrame()
# while line_sn <= len(filedate):
#     tst_file = filedate[line_sn-1]
#     if tst_file[1] == 0:
#         line_sn = line_sn + 1
#         continue
#     break
#
#
# # just replace the filename with file from the server named by filedate
# tst_filename = '%sRO_History%s.csv' % (data_dir, tst_file[0])
# raw_tst_df = pd.read_csv('%s' % tst_filename)
# tst_df = pd.pivot_table(raw_tst_df, values='VarValue', index=['TimeString'], columns=['VarName'])
# if '$RT_OFF$' in tst_df.columns:
#     tst_df.drop(['$RT_OFF$'], axis = 1, inplace = True)
# if tst_df.index.name != 'TimeString':
#     tst_df.set_index(['TimeString'], drop = True, inplace = True)
# tst_df.dropna(inplace = True)
# X_tst= tst_df[explanatory_names]
# y_tst = tst_df[explained_names]
# tst_obj = md_obj.testing_handler(X_tst, y_tst, trn_obj, extend_degree)
# md_obj.plot_model_phase(tst_obj, trn_obj, 'BeerGordon', explained_names, explanatory_names, extend_degree, 'testing', plot_dir)
# print('')






md_obj = MultiDimensionalModeling()
trn_obj = None

def make_training(df,inner_sensors, outer_sensors ):
    global trn_obj
    # explained_names = [sensors[index] for index, v in enumerate(role) if v == 'explained']
    # explanatory_names = [sensors[index] for index, v in enumerate(role) if v == 'explanatory']

    X_trn = df[outer_sensors]
    y_trn = df[inner_sensors]

    trn_obj = md_obj.training_handler(X_trn, y_trn, extend_degree)
    # md_obj.plot_model_phase(trn_obj, trn_obj, 'BeerGordon', explained_names, explanatory_names, extend_degree, 'training', plot_dir)

def make_testing(df, inner_sensors, outer_sensors):
    global trn_obj
    # explained_names = [sensors[index] for index, v in enumerate(role) if v == 'explained']
    # explanatory_names = [sensors[index] for index, v in enumerate(role) if v == 'explanatory']
    if not trn_obj:
        return "Training object is not initialized, please train the system"
    X_tst = df[outer_sensors]
    y_tst = df[inner_sensors]
    tst_obj = md_obj.testing_handler(X_tst, y_tst, trn_obj, extend_degree)
    # md_obj.plot_model_phase(tst_obj, trn_obj, 'BeerGordon', explained_names, explanatory_names, extend_degree,
    #                         'testing', plot_dir)
    return compute_result(tst_obj, trn_obj.ylw_thr, trn_obj.red_thr)



def compute_result(tst_obj, yellow_threshold, red_threshold):
    result = []
    # tst_obj.residuals_df is not sorted by "timestring" its sorted by ActValue from minimal to maximal
    for i, val in enumerate(tst_obj.residuals_df['ActValue']):
        if val < yellow_threshold:
            result.append((tst_obj.residuals_df.index[i], HealthGrade.HG_GOOD))
        elif yellow_threshold <= val < red_threshold:
            result.append((tst_obj.residuals_df.index[i], HealthGrade.HG_ALARM))
        else:
            result.append((tst_obj.residuals_df.index[i], HealthGrade.HG_CRITICAL))
    logger.info(result)
    return result

def convert_received_object(buffer_obj):
    obj = pickle.loads(buffer_obj)
    dataframe = obj.get('dataframe')
    method = obj.get('method')
    inner_sensors = obj.get('inner_sensors')
    outer_sensors = obj.get('outer_sensors')
    return method, dataframe, inner_sensors, outer_sensors


# Main loop.
logger.info("math engine is waiting for connections. ")
while True:
    ret_obj = {}
    SUCCESS = 0
    FAILURE = 1
    #  Wait for next request from client
    message = socket.recv()
    method, dataframe, inner_sensors, outer_sensors = convert_received_object(message)
    ret_obj['method'] = method
    try:
        if method == "train":
            make_training(dataframe, inner_sensors, outer_sensors)
            ret_obj['result'] = None
            ret_obj['status'] = SUCCESS
            ret_obj['msg'] = "Training finished "
        elif method == "test":
            ret_obj['result'] = make_testing(dataframe, inner_sensors, outer_sensors)
            ret_obj['status'] = SUCCESS
            ret_obj['msg'] = "Testing finished "
    except Exception as e:
        logger.error(traceback.format_exc())
        ret_obj['status'] = FAILURE
        ret_obj['msg'] = traceback.format_exc()

    socket.send(pickle.dumps(ret_obj))


# Todo - main entrance to math_engine
# Todo - read config and initialise logger .
# Todo - add main loop
# Todo - remove plots



