import cv2
import numpy
# import scipy.signal as sg
from bgArrayLogger import *
from .tool_functions import *


class ArchiveError(Exception):
    """Base class for exceptions."""

    def __init__(self, *args):
        super().__init__(*args)


class DifferenceError(ArchiveError):  # 当计算差值列表的众数和中位数的差值过大时抛出
    pass


def lineO_hProjectionAnalyse(inI: list, width: int = None):
    """
    :param inI 输入的getHProjection()的返回值，是一个list包含每一行的white pix count
    :param width 输入的图片宽度，用以相减获得每一行black pix count，默认None
    """
    h_list = []
    if width is not None:
        for i in inI:
            h_list.append(width - i)
    else:
        h_list = inI
    h_list = numpy.array(h_list)
    # print(h_list)

    continuous = lineO_hProjectionContinuousScanning(h_list)
    logger.info("continuous: " + str(continuous))
    # continuous = l2

    # max_in = numpy.argmax(h_list)
    # logger.info(max_in)
    # print(h_list[numpy.argmax(h_list)])
    # print(sg.argrelmax(h_list))  # 极大值 的下标
    # logger.info(str(sg.argrelmax(h_list)))
    index = 0
    max_round = []  # 较大线段的纵坐标
    for i in h_list:
        if i in range(h_list[numpy.argmax(h_list)] - 31, h_list[numpy.argmax(h_list)] + 1):
            # print(i)
            max_round.append(index)
        index += 1
    logger.info("较大线段的纵坐标: " + str(max_round))

    difference = lineO_hProjectionMaxClassifier(max_round)
    logger.info("[分界线, 平均线宽]: " + str(difference))
    base_line = average(difference)

    diff_arr = []
    # 遍历数组，计算每两个数之间的差
    for i in range(len(max_round) - 1):
        diff_arr.append(max_round[i + 1] - max_round[i])

    lines_group = []
    now_group = []
    index = 0
    long_ = max_round.__len__()
    for i in max_round:
        if index == 0:
            now_group.append(i)
        elif index == long_ - 1:
            now_group.append(i)
            lines_group.append(now_group)
        else:
            if diff_arr[index - 1] <= base_line:
                now_group.append(i)
            else:
                lines_group.append(now_group)
                now_group = [i]
        index += 1
    logger.info("五线谱纵坐标: " + str(lines_group))


def lineO_hProjectionContinuousScanning(inL: numpy.ndarray) -> list:
    """
    返回连续像素范围
    :param inL 输入的数组
    :return 一个list  像这样：
    [{'white': [0, 152]}, {'black': [153, 246]}, {'white': [247, 255]}, ..., {'black': [2203, 2224]},
    {'white': [2225, 2338]}]
    """
    return_list = []
    now_list = []
    now_state = -1  # -1: nothing(init) 0 white; 1 black
    index = 0
    for i in inL:
        if i == 0 and now_list == [] and now_state == -1:
            now_list.append(index)
            now_state = 0
        elif i != 0 and now_list != [] and now_state == 0:
            now_list.append(index - 1)
            return_list.append({"white": now_list})
            now_list = [index]
            now_state = 1
        elif i == 0 and now_list != [] and now_state == 1:
            now_list.append(index - 1)
            return_list.append({"black": now_list})
            now_list = [index]
            now_state = 0

        index += 1

    if now_list != [] and now_state == 0:
        now_list.append(index - 1)
        return_list.append({"white": now_list})
    elif now_list != [] and now_state == 1:
        now_list.append(index - 1)
        return_list.append({"black": now_list})

    logger.info(return_list)

    return return_list


def lineO_hProjectionMaxClassifier(inL: list) -> list:
    """
    :param inL 输入列表

    :return: 输出列表：[31, 12] [分界线, 平均线宽]
    """
    # 计算每两个数之间的差
    # 定义一个空列表，用来存储每两个数之间的差
    diff_arr = []
    # 遍历数组，计算每两个数之间的差
    for i in range(len(inL) - 1):
        diff_arr.append(inL[i + 1] - inL[i])

    a_m_m = average_median_mode(diff_arr)

    if a_m_m[1] == a_m_m[2]:
        return [a_m_m[0], a_m_m[1]]
    else:
        if a_m_m[1] - a_m_m[2] <= 2:
            return [a_m_m[0], a_m_m[2]]
        else:
            raise DifferenceError("当计算差值列表的众数和中位数的差值过大时抛出")
