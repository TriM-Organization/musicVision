from ._main import *
import objectStateConstants as osc
import exceptions
import copy
import numpy


debugger = osc.ObjectStateConstant()
# print(debugger.isDebugging)


class SheetVisionLib:
    def __init__(self):
        self.pic_path = {}
        self.is_pic_path = False

        self.pic_class = {}  # 图像数组
        self.pic_datas = {}  # 图像数据

        self.now_pic = numpy.ndarray([])
        self.now_img_width = 0
        self.now_img_height = 0
        self.now_pic_grey = numpy.ndarray([])

    def pictures_path_load(self, value: dict) -> None:
        for i_ in ["staff_files", "quarter_files", "sharp_files", "flat_files", "half_files", "whole_files"]:
            if i_ in value.keys():
                for j_ in value[i_]:
                    if j_[j_.__len__() - 3:] not in ["jpg", "png", "gif", "pmb"]:
                        raise exceptions.FormatError
                    else:
                        pass
            else:
                raise exceptions.MissingContentError

        self.pic_path = value
        self.is_pic_path = True
        debugger.dp(self.pic_path)

    def pictures_reload(self) -> None:
        if self.is_pic_path is not True:
            print("please set path at first.")
            raise exceptions.NotLoadedError
        self.pic_class = copy.copy(self.pic_path)
        for imgs_type in self.pic_path.keys():
            index = 0
            for img_files in self.pic_path[imgs_type]:
                self.pic_class[imgs_type][index] = cv2.imread(img_files, 0)
                # https://blog.csdn.net/qq_37924224/article/details/119181028
        if debugger.isDebugging:
            for i_ in self.pic_class.keys():
                debugger.dp(self.pic_class[i_].__len__())
            debugger.dp("class list(use for test)")
            debugger.dp(self.pic_class)

    def pictures_data_load(self, in_dict: dict) -> None:
        self.pic_datas = in_dict

    @staticmethod
    def abbreviation_expansion(in_dict: dict) -> dict:
        if list(in_dict.keys())[0] != "#":
            raise exceptions.InformationGone

        info = in_dict.get("#")
        expansion = {}

        for j_ in in_dict.keys():
            if j_ == "#":
                continue
            else:
                list_expan = {}
                index = 0
                for i_ in info:
                    list_expan[i_] = in_dict[j_][index]
                    index += 1
                expansion[j_] = list_expan
        debugger.dp(expansion)
        return expansion

    @staticmethod
    def pictures_locating(img_, templates, start, stop, threshold):
        re = locate_images(img_, templates, start, stop, threshold)
        return re

    @staticmethod
    def merge_rectangles(recs, threshold):
        re = merge_recs(recs, threshold)
        return re

    @staticmethod
    def show_pic(path: str) -> None:
        open_file(path)

    def pictures_initialize(self, in_path: str) -> None:
        img_file_ = os.path.abspath(in_path)
        self.now_pic = cv2.imread(img_file_, 0)
        if self.now_pic is None:
            raise exceptions.PictureNotExist

        # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        self.now_pic_grey = self.now_pic
        self.now_pic = cv2.cvtColor(self.now_pic_grey, cv2.COLOR_GRAY2RGB)
        ret_, now_pic_grey = cv2.threshold(self.now_pic_grey, 127, 255, cv2.THRESH_BINARY)
        del ret_
        self.now_img_width, self.now_img_height = now_pic_grey.shape[::-1]

        # cv.cvtColor(	src, code[, dst[, dstCn]]
        # 色彩空间转化

        # cv.threshold( src, thresh, maxval, type[, dst] )
        # thresh：当前阈值。
        # maxVal：最大阈值，一般为255.
        # 去掉噪点
        # https://blog.csdn.net/weixin_42296411/article/details/80901080

        # cv.shape
        # 有一张图片宽度*高度是300*100，用opencv的img.shape返回的是(100,300,3)，
        # shape返回的是图像的行数，列数，色彩通道数。
        # 易错的地方：
        # 行数其实对应于坐标轴上的y，即表示的是图像的高度
        # 列数对应于坐标轴上的x，即表示的是图像的宽度
        # 也就是说shape返回的是(高度， 宽度) = (y , x)
        # 而
        # img[50,10]是否表示是(x,y)为(50,10)的那个像素呢，其实不是。
        # 与shape的原理相同，它表示的也是(y,x)，即表示第50列第10行的那个元素。
        # ————————————————
        # 版权声明：本文为CSDN博主「天地一扁舟」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
        # 原文链接：https://blog.csdn.net/qingyuanluofeng/article/details/51568741

    def sample_match(self):
        pass

    def analysis(self):
        pass

    def midi_dump(self):
        pass

# self.staff_files = []
# self.quarter_files = []
# self.sharp_files = []
# self.flat_files = []
# self.half_files = []
# self.whole_files = []
#
# self.staff_imgs = []
# self.quarter_imgs = []
# self.sharp_imgs = []
# self.flat_imgs = []
# self.half_imgs = []
# self.whole_imgs = []

# self.staff_files = self.pic_path["staff_files"]
# self.quarter_files = self.pic_path["quarter_files"]
# self.sharp_files = self.pic_path["sharp_files"]
# self.flat_files = self.pic_path["flat_files"]
# self.half_files = self.pic_path["half_files"]
# self.whole_files = self.pic_path["whole_files"]

# self.staff_imgs = [cv2.imread(staff_file, 0) for staff_file in self.staff_files]
# self.quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in self.quarter_files]
# self.sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in self.sharp_files]
# self.flat_imgs = [cv2.imread(flat_file, 0) for flat_file in self.flat_files]
# self.half_imgs = [cv2.imread(half_file, 0) for half_file in self.half_files]
# self.whole_imgs = [cv2.imread(whole_file, 0) for whole_file in self.whole_files]

# staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
# quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
# sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
# flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
# half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
# whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]
