import cv2
import numpy
# import scipy.signal as sg
from bgArrayLogger import *


def lineO_hProjectionAnalyse(inI: list, weight: int = None):
    h_list = []
    if weight is not None:
        for i in inI:
            h_list.append(weight - i)
    else:
        h_list = inI
    h_list = numpy.array(h_list)
    print(h_list)
    max_in = numpy.argmax(h_list)
    logger.info(max_in)
    # print(h_list[numpy.argmax(h_list)])
    # print(sg.argrelmax(h_list))  # 极大值 的下标
    # logger.info(str(sg.argrelmax(h_list)))
    index = 0
    max_round = []
    for i in h_list:
        if i in range(h_list[numpy.argmax(h_list)] - 21, h_list[numpy.argmax(h_list)] + 1):
            print(i)
            max_round.append(index)
        index += 1
    print(max_round)
