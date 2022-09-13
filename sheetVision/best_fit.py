import cv2
import matplotlib.pyplot as plt
import numpy as np


def fit(img, templates, start_percent, stop_percent, threshold):
    """
    匹配函数
    :param img: 输入图像
    :param templates: 输入模板？
    :param start_percent: 起始百分比
    :param stop_percent: 结束百分比
    :param threshold: n.门槛；门口；阈；界；起始点；开端；起点；入门
    """
    img_width, img_height = img.shape[::-1]
    best_location_count = -1
    best_locations = []
    best_scale = 1

    plt.axis([0, 2, 0, 1])  # plt.axis([a, b, c, d])  设置x轴的范围为[a, b]，y轴的范围为[c, d]
    plt.show(block=False)  # 显示绘图，但不启用阻塞模式，意思为显示图片后仍然执行程序而非展示图片时程序暂停。
    # plt.show(block=True)

    x = []
    y = []
    # scale n.音阶
    for scale in [i / 100.0
                  for i in range(start_percent, stop_percent + 1, 3)]:
        locations = []
        location_count = 0
        for template in templates:
            template = cv2.resize(template, None,
                                  fx=scale, fy=scale, interpolation=cv2.INTER_CUBIC)
            result = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)
            result = np.where(result >= threshold)
            location_count += len(result[0])
            locations += [result]
        print("scale: {0}, hits: {1}".format(scale, location_count))
        x.append(location_count)
        y.append(scale)
        plt.plot(y, x)
        plt.pause(0.00001)
        if location_count > best_location_count:
            best_location_count = location_count
            best_locations = locations
            best_scale = scale
            plt.axis([0, 2, 0, best_location_count])
        elif location_count < best_location_count:
            pass
    plt.close()

    print(best_locations)
    print(best_scale)
    # print(5/0)

    return best_locations, best_scale
