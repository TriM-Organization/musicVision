import cv2
import numpy


def max_min(inI: numpy.ndarray) -> list:
    imageI = inI
    print(imageI)

    canny = cv2.Canny(imageI, 80, 160, 3)
    # cv2.imshow("Canny Image", canny)
    cv2.imwrite("Canny.png", canny)

    kernel = cv2.getStructuringElement(0, (3, 3))
    canny = cv2.dilate(canny, kernel)

    contours, hierarchy = cv2.findContours(canny, mode=0, method=2)

    img1 = imageI.copy()
    img2 = imageI.copy()

    maxPointList = []
    minPointList = []
    for i in range(contours.__len__()):
        max_rect = cv2.boundingRect(contours[i])
        # print(max_rect)
        # points = cv2.boxPoints(max_rect).astype(numpy.int64)
        # print(points)
        maxPointList.append(max_rect)
        cv2.rectangle(img1, max_rect, (0, 0, 255), 2, 8, 0)

        min_rect = cv2.minAreaRect(contours[i])
        # print(min_rect)
        points = cv2.boxPoints(min_rect).astype(numpy.int64)
        # print(points)
        minPointList.append(points)
        img2 = cv2.drawContours(img2, [points], -1, (0, 255, 0), 2, 8)

    # cv2.imshow("MAX", img1)
    # cv2.imshow("MIN", img2)

    cv2.imwrite("Max.png", img1)
    cv2.imwrite("Min.png", img2)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    return [maxPointList, minPointList]


def obfuscation(inI: numpy.ndarray, array: int = 13, weight: float = 2.0) -> numpy.ndarray:
    img = inI
    dst3 = cv2.GaussianBlur(img, (array, array), weight)
    return dst3
    # cv2.imwrite("GaussianBlur.png", dst3)


def dilate_r(inI: numpy.ndarray, kernel_in: int = 7, is_erosion: bool = True) -> numpy.ndarray:
    src = inI

    # b.设置卷积核5*5
    kernel = numpy.ones((kernel_in, kernel_in), numpy.uint8)
    # c.图像的腐蚀，默认迭代次数
    if is_erosion:
        erosion = cv2.erode(src, kernel)
        # 图像的膨胀
        dst = cv2.dilate(erosion, kernel)
    else:
        dst = cv2.dilate(src, kernel)

    cv2.imwrite("dilate.png", dst)

    return dst


# 两个检测框框是否有交叉，如果有交集则返回重叠度 IOU, 如果没有交集则返回 0
def bb_over_lab(x1, y1, w1, h1, x2, y2, w2, h2):
    """
    说明：图像中，从左往右是 x 轴（0~无穷大），从上往下是 y 轴（0~无穷大），从左往右是宽度 w ，从上往下是高度 h
    :param x1: 第一个框的左上角 x 坐标
    :param y1: 第一个框的左上角 y 坐标
    :param w1: 第一幅图中的检测框的宽度
    :param h1: 第一幅图中的检测框的高度
    :param x2: 第二个框的左上角 x 坐标
    :param y2:
    :param w2:
    :param h2:
    :return: 两个如果有交集则返回重叠度 IOU, 如果没有交集则返回 0
    """
    # https://blog.csdn.net/tutu96177/article/details/87784058
    if x1 > x2 + w2:
        return 0
    if y1 > y2 + h2:
        return 0
    if x1 + w1 < x2:
        return 0
    if y1 + h1 < y2:
        return 0
    colInt = abs(min(x1 + w1, x2 + w2) - max(x1, x2))
    rowInt = abs(min(y1 + h1, y2 + h2) - max(y1, y2))
    overlap_area = colInt * rowInt
    area1 = w1 * h1
    area2 = w2 * h2
    return overlap_area / (area1 + area2 - overlap_area)


def merge_min_rectangles(img: numpy.ndarray, inI: list[numpy.ndarray, numpy.ndarray]):
    merge_list = inI[1]
    try:
        contours_merge = numpy.vstack([merge_list[0], merge_list[1]])
    except IndexError:
        # merge_res = max_min(img)[1]
        # print(merge_res)
        # cv2.imwrite("merge_min.png", merge_res)
        return 0
    for i in range(2, len(merge_list)):
        contours_merge = numpy.vstack([contours_merge, merge_list[i]])

    rect2 = cv2.minAreaRect(contours_merge)
    box2 = cv2.boxPoints(rect2)
    box2 = numpy.int0(box2)
    merge_res = cv2.drawContours(img, [box2], 0, (0, 255, 0), 2)

    cv2.imwrite("merge_min.png", merge_res)


'''水平投影'''


def getHProjection(image: numpy.ndarray):
    hProjection = numpy.zeros(image.shape, numpy.uint8)
    # 图像高与宽
    (h, w) = image.shape
    # 长度与图像高度一致的数组
    h_ = [0] * h
    # 循环统计每一行白色像素的个数
    for y in range(h):
        for x in range(w):
            if image[y, x] == 255:
                h_[y] += 1
    # 绘制水平投影图像
    for y in range(h):
        for x in range(h_[y]):
            hProjection[y, x] = 255
    cv2.imwrite('hProjection2.png', hProjection)

    return h_


def round_up(num, power=0):
    """
    实现精确四舍五入，包含正、负小数多种场景
    :param num: 需要四舍五入的小数
    :param power: 四舍五入位数，支持0-∞
    :return: 返回四舍五入后的结果
    """
    try:
        print(1 / 0)
    except ZeroDivisionError:
        digit = 10 ** power
        num2 = float(int(num * digit))
        # 处理正数，power不为0的情况
        if num >= 0 and power != 0:
            tag = num * digit - num2 + 1 / (digit * 10)
            if tag >= 0.5:
                return (num2 + 1) / digit
            else:
                return num2 / digit
        # 处理正数，power为0取整的情况
        elif num >= 0 and power == 0:
            tag = num * digit - int(num)
            if tag >= 0.5:
                return (num2 + 1) / digit
            else:
                return num2 / digit
        # 处理负数，power为0取整的情况
        elif power == 0 and num < 0:
            tag = num * digit - int(num)
            if tag <= -0.5:
                return (num2 - 1) / digit
            else:
                return num2 / digit
        # 处理负数，power不为0的情况
        else:
            tag = num * digit - num2 - 1 / (digit * 10)
            if tag <= -0.5:
                return (num2 - 1) / digit
            else:
                return num2 / digit


def delete_extra_zero(n: float) -> int or float:
    """
    删除多余的0
    ————————————————
    版权声明：本文为CSDN博主「XerCis」的原创文章，遵循CC 4.0 BY-SA版权协议，转载请附上原文出处链接及本声明。
    原文链接：https://blog.csdn.net/lly1122334/article/details/108770141
    删除小数点后多余的0
    :param n: input
    :return:  output
    """
    n = '{:g}'.format(n)
    n = float(n) if '.' in n else int(n)  # 含小数点转float否则int
    return n


# 平均数
def average(nums, is_round_up=False):
    if is_round_up is False:
        return sum(nums) / len(nums)
    else:
        return delete_extra_zero(round_up(sum(nums) / len(nums)))


# 中位数
def median(nums):
    nums.sort()
    size = len(nums)
    if size % 2 == 0:
        return (nums[size // 2 - 1] + nums[size // 2]) / 2
    else:
        return nums[(size - 1) // 2]


# 众数
def mode_n(nums):
    from collections import Counter
    count = Counter(nums)
    max_count = max(count.values())
    modes = [k for k, v in count.items() if v == max_count][0]
    return modes


def average_median_mode(inL: list) -> tuple:
    return average(inL, True), median(inL), mode_n(inL)
