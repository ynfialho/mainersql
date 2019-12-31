import logging
from sys import stdout
import os
from datetime import datetime

def setting_log(flag_stdout=True, flag_logfile=False):
    """
    Applies log settings and returns a logging object.
    :flag_stdout: boolean
    :flag_logfile: boolean
    """
    handler_list = list()
    LOGGER = logging.getLogger()
    [LOGGER.removeHandler(h) for h in LOGGER.handlers]

    if flag_logfile:
        path_log = './logs/{}_{:%Y%m%d}.log'.format('log', datetime.now())
        if not os.path.isdir('./logs'):
            os.makedirs('./logs')
        handler_list.append(logging.FileHandler(path_log))

    if flag_stdout:
        handler_list.append(logging.StreamHandler(stdout))
        
    logging.basicConfig(
        level=logging.INFO\
        ,format='[%(asctime)s] {%(filename)s:%(lineno)d} %(levelname)s - %(message)s'\
        ,handlers=handler_list)    
    return LOGGER


