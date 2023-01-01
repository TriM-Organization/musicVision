import os.path
import cv2.cv2
# import numpy
from sheetVisionLib.lineOperation import *


class DataMaker:
    def __init__(self, in_path: str):
        self.now_pic = numpy.ndarray([])  # 目前操作目标图片
        self.now_img_width = 0  # 宽
        self.now_img_height = 0  # 高
        self.now_pic_grey = numpy.ndarray([])  # 灰度图片
        self.now_hProjection = numpy.ndarray([])
        # print(in_path)
        self.in_path = in_path.replace("data\\", "data\\pic\\")
        self.is_pdf = False
        self.name_list = []
        if self.in_path.endswith(".pdf"):
            self.is_pdf = True
            self.pdf_to_pic()
            self.pictures_initialize()
        else:
            self.pictures_initialize()

    def pictures_initialize(self) -> None:
        if self.is_pdf is False:
            print(os.path.abspath(self.in_path))
            img_file_ = os.path.abspath(self.in_path)
            self.now_pic = cv2.imread(img_file_, 0)

            # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            self.now_pic_grey = self.now_pic
            # self.now_pic = cv2.cvtColor(self.now_pic_grey, cv2.COLOR_GRAY2RGB)
            ret_, self.now_pic_grey = cv2.threshold(self.now_pic_grey, 127, 255, cv2.THRESH_BINARY)
            del ret_
            self.now_img_width, self.now_img_height = self.now_pic_grey.shape[::-1]

            self.now_hProjection = getHProjection(self.now_pic_grey, self.in_path.replace(".png", "hp.png"))
            # print(self.now_hProjection)
            # cv2.imwrite(self.in_path.replace(".png", "hp.png"), self.now_hProjection)
            lineO_hProjectionAnalyse(self.now_hProjection, self.now_img_width, False)
        else:
            for index in self.name_list:
                print(index)
                img_file_ = os.path.abspath(index)
                self.now_pic = cv2.imread(img_file_, 0)

                # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                self.now_pic_grey = self.now_pic
                # self.now_pic = cv2.cvtColor(self.now_pic_grey, cv2.COLOR_GRAY2RGB)
                ret_, self.now_pic_grey = cv2.threshold(self.now_pic_grey, 127, 255, cv2.THRESH_BINARY)
                del ret_
                self.now_img_width, self.now_img_height = self.now_pic_grey.shape[::-1]

                self.now_hProjection = getHProjection(self.now_pic_grey, index.replace(".png", "hp.png"))
                # cv2.imwrite(index.replace(".png", "hp.png"), self.now_hProjection)
                lineO_hProjectionAnalyse(self.now_hProjection, self.now_img_width, False)

    def pdf_to_pic(self):
        # from pdf2image.exceptions import (
        #     PDFInfoNotInstalledError,
        #     PDFPageCountError,
        #     PDFSyntaxError
        # )
        # from PIL import Image
        from pdf2image import convert_from_path  # , convert_from_bytes

        images = convert_from_path(self.in_path)
        # print(images)
        count = 0
        for k in range(images.__len__()):
            images[k].save(os.path.abspath(self.in_path).replace(".pdf", str(count) + ".png"))
            self.name_list.append(os.path.abspath(self.in_path).replace(".pdf", str(count) + ".png"))
            count += 1
        # images = convert_from_bytes(open('破云来（Shrimp）.pdf', 'rb').read())


if __name__ == '__main__':
    for i in os.listdir("./pic"):
        if i.endswith("hp.png"):
            continue
        else:
            DataMaker(os.path.abspath(i))
