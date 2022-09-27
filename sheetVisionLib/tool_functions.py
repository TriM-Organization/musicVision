import cv2
import numpy


def scanning(inI):
    imageI = cv2.imread(inI)

    canny = cv2.Canny(imageI, 80, 160, 3)
    # cv2.imshow("Canny Image", canny)
    cv2.imwrite("./pic/tdst/tdst-01Canny.png", canny)

    kernel = cv2.getStructuringElement(0, (3, 3))
    canny = cv2.dilate(canny, kernel)

    contours, hierarchy = cv2.findContours(canny, mode=0, method=2)

    img1 = imageI.copy()
    img2 = imageI.copy()

    minPointList = []
    for i in range(contours.__len__()):
        max_rect = cv2.boundingRect(contours[i])
        # print(max_rect)
        # points = cv2.boxPoints(max_rect).astype(numpy.int64)
        # print(points)
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

    return minPointList