import logging
import uuid
import datetime
import os
# import sys

import objectStateConstants

debugger = objectStateConstants.ObjectStateConstant()

version = "v0.2.1"


def copyrightVersion():
    global version
    logger.info("------------------------------------------------")
    logger.info("正在使用：bgArray的logger库，版权归bgArray所有")
    logger.info("版本号：" + version)
    logger.info("------------------------------------------------\n")


def logChi_Eng(inp: tuple, level: str = "info"):
    if level == "info":
        logger.info(inp[0] + "-" + inp[1])


class DoNOT:
    def info(self, inThing):
        pass

    def debug(self, inThing):
        pass

    def warning(self, inThing):
        pass

    def error(self, inThing):
        pass


if debugger.isLoggingUsing:
    StrStartTime = str(datetime.datetime.now()).replace(':', '_')[:-7]

    logger = logging.getLogger(__name__)
    logger.setLevel(level=logging.DEBUG)
    try:
        handler = logging.FileHandler("./log/log" + StrStartTime + " " + str(uuid.uuid4()) + ".log.txt",
                                      encoding="utf-8")
    except FileNotFoundError:
        os.mkdir("./log/")
        handler = logging.FileHandler("./log/log" + StrStartTime + " " + str(uuid.uuid4()) + ".log.txt",
                                      encoding="utf-8")
    handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)

    copyrightVersion()

else:
    logger = DoNOT()
