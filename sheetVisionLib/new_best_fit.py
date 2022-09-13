import cv2
# import matplotlib.pyplot as plt
import numpy as np


def fit(img: np.ndarray, templates: list, start_percent: int, stop_percent: int,
        threshold: float) -> tuple[list, float]:
    """
    匹配函数
    :param img: 输入图像
    :param templates: 输入模板，这里指的是在main.py中，初始化时打开的预制图片，用于匹配，路径为"resources/template/xxxxx.png"
    :param start_percent: 起始百分比
    :param stop_percent: 结束百分比
    :param threshold: n.门槛；门口；阈；界；起始点；开端；起点；入门

    :return: best_locations, best_scale(x轴最佳坐标,y轴最佳比例)
    """
    # img_width, img_height = img.shape[::-1]

    best_location_count = -1
    best_locations = []
    best_scale = 1

    # plt.axis([0, 2, 0, 1])  # plt.axis([a, b, c, d])  设置x轴的范围为[a, b]，y轴的范围为[c, d]
    # plt.show(block=False)  # 显示绘图，但不启用阻塞模式，意思为显示图片后仍然执行程序而非展示图片时程序暂停。
    # plt.show(block=True)

    x = []
    y = []
    # scale n.比例
    scale_range = []  # 逐步放大的比例值，所以下面resize时的插值方法选了适合放大效果的cv.INTER_CUBIC
    for i in range(start_percent, stop_percent + 1, 3):
        scale_range.append(i / 100.0)
    print(scale_range)

    for scale in scale_range:
        locations = []
        location_count = 0
        for template in templates:  # 这里需要让每一个模板都匹配一次
            # resize()函数用于尺寸变换 书65页
            # cv.resize(src, dsize [, dst [, fx [, fy [, interpolation ]]]])
            # src:输入图片
            # dsize:输出图片尺寸
            # dst:输出图片
            # fx/fy:沿x轴，y轴的缩放系数(指定为2，则该轴放大2倍)
            # interpolation:插入方式
            template = cv2.resize(template, None,
                                  fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)  # 按照比例值放大图片

            # matchTemplate()函数用于图像模板匹配 书114页
            # matchTemplate(image, templ, method [,result [, mask ]])
            # image:原图像
            # templ:模板
            # method:匹配方法
            # result:结果图像
            # mask:匹配模板掩模
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)  # 以归一化相关系数匹配法(TM_CCOEFF_NORMED)匹配
            result = np.where(result >= threshold)  # 找出数组中满足结果的(>=门槛值)
            location_count += len(result[0])  # 统计符合条件的点数
            locations += [result]  # 坐标获取
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)  # x轴用匹配点
        y.append(scale)  # y轴用比例
        # plt.plot(y, x)
        # plt.pause(0.00001)
        if location_count > best_location_count:  # 逐一循环比大小，类似于pop
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            # plt.axis([0, 2, 0, best_location_count])
        elif location_count < best_location_count:
            pass
    # plt.close()

    # print(best_locations)
    # print(best_scale)

    return best_locations, best_scale  # 返回最优解
