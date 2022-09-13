import os.path
import sys
import subprocess
import cv2
# import time
import numpy as np
from .new_best_fit import fit
from .rectangle import Rectangle
from .note import Note
from random import randint
from .midiutil.MidiFile3 import MIDIFile


# ORB特征点匹配图像载入

# 1.路径设置
staff_files = [
    "./sheetVisionLib/resources/template/staff2.png",
    "./sheetVisionLib/resources/template/staff.png"]
quarter_files = [
    "./sheetVisionLib/resources/template/quarter.png",
    "./sheetVisionLib/resources/template/solid-note.png"]
sharp_files = [
    "./sheetVisionLib/resources/template/sharp.png"]
flat_files = [
    "./sheetVisionLib/resources/template/flat-line.png",
    "./sheetVisionLib/resources/template/flat-space.png"]
half_files = [
    "./sheetVisionLib/resources/template/half-space.png",
    "./sheetVisionLib/resources/template/half-note-line.png",
    "./sheetVisionLib/resources/template/half-line.png",
    "./sheetVisionLib/resources/template/half-note-space.png"]
whole_files = [
    "./sheetVisionLib/resources/template/whole-space.png",
    "./sheetVisionLib/resources/template/whole-note-line.png",
    "./sheetVisionLib/resources/template/whole-line.png",
    "./sheetVisionLib/resources/template/whole-note-space.png"]

switch = False
# 2.图片对象在cv中打开
if switch:
    staff_imgs = [cv2.imread(staff_file, 0) for staff_file in staff_files]
    quarter_imgs = [cv2.imread(quarter_file, 0) for quarter_file in quarter_files]
    sharp_imgs = [cv2.imread(sharp_files, 0) for sharp_files in sharp_files]
    flat_imgs = [cv2.imread(flat_file, 0) for flat_file in flat_files]
    half_imgs = [cv2.imread(half_file, 0) for half_file in half_files]
    whole_imgs = [cv2.imread(whole_file, 0) for whole_file in whole_files]

# 3.匹配数据载入
staff_lower, staff_upper, staff_thresh = 50, 150, 0.77
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70


def locate_images(img_, templates, start, stop, threshold):  # 匹配函数调用
    locations, scale = fit(img_, templates, start, stop, threshold)
    img_locations = []
    for i in range(len(templates)):
        w, h = templates[i].shape[::-1]  # 长宽 width, height
        w *= scale
        h *= scale
        img_locations.append([Rectangle(pt[0], pt[1], w, h)
                             for pt in zip(*locations[i][::-1])])  # [::-1]倒序复制
        # print(list(zip(*locations[i][::-1]))) 坐标
        # append_things = []
        # for pt in zip(*locations[i][::-1]):
        #     append_things.append(Rectangle(pt[0], pt[1], w, h))
        # img_locations.append(append_things)
    return img_locations


def merge_recs(recs, threshold):  # 合并Rectangle类 threshold n.门槛
    filtered_recs = []  # 过滤完的 (处理过的)
    while len(recs) > 0:
        r = recs.pop(0)  # 取出打头项
        recs.sort(key=lambda rec: rec.distance(r))
        # def keyM(rec):
        #     return rec.distance(r)
        # recs.sort(key=keyM())
        merged = True
        while merged:
            merged = False
            i = 0
            for _ in range(len(recs)):
                if r.overlap(
                        recs[i]) > threshold or recs[i].overlap(r) > threshold:
                    r = r.merge(recs.pop(i))
                    merged = True
                elif recs[i].distance(r) > r.w / 2 + recs[i].w / 2:
                    break
                else:
                    i += 1
        filtered_recs.append(r)
    # print(filtered_recs)
    return filtered_recs


def open_file(path: str) -> None:  # 展示图片文件函数
    cmd = {'linux': 'eog', 'win32': 'explorer', 'darwin': 'open'}[sys.platform]
    subprocess.run([cmd, path])


if __name__ == "__main__":
    # print(sys.argv[1:][0])
    # img_file = sys.argv[1:][0]
    # img_file = "./inImg/test0.png"
    img_file = os.path.abspath("./inImg/s2-1.png")
    img = cv2.imread(img_file, 0)
    img_gray = img  # cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # cv.cvtColor(	src, code[, dst[, dstCn]]
    # 色彩空间转化
    img = cv2.cvtColor(img_gray, cv2.COLOR_GRAY2RGB)

    # cv.threshold( src, thresh, maxval, type[, dst] )
    # thresh：当前阈值。
    # maxVal：最大阈值，一般为255.
    # 去掉噪点
    # https://blog.csdn.net/weixin_42296411/article/details/80901080
    ret, img_gray = cv2.threshold(img_gray, 127, 255, cv2.THRESH_BINARY)

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
    img_width, img_height = img_gray.shape[::-1]

    print("Matching staff image...")
    print("正在匹配空白五线谱图像...")

    staff_recs = locate_images(
        img_gray,
        staff_imgs,
        staff_lower,
        staff_upper,
        staff_thresh)

    print("Filtering weak staff matches...")
    print("正在筛选弱空白五线谱匹配...")

    staff_recs = [j for i in staff_recs for j in i]
    # staff_recs = []
    # for i in staff_recs:
    #     for j in i:
    #         staff_recs.append(j)
    heights = [r.y for r in staff_recs] + [0]
    # heights = []
    # for r in staff_recs:
    #     heights.append(r.y)
    # heights.append(0)
    histo = [heights.count(i) for i in range(0, max(heights) + 1)]
    # histo = []
    # for i in range(0, max(heights) + 1):
    #     histo.append(heights.count(i))
    avg = np.mean(list(set(histo)))  # 求列表平均值
    staff_recs = [r for r in staff_recs if histo[r.y] > avg]
    # staff_recs = []
    # for r in staff_recs:
    #     if histo[r.y] > avg:
    #         staff_recs.append(r)

    print("Merging staff image results...")
    print("正在合并空白五线谱图像结果...")
    staff_recs = merge_recs(staff_recs, 0.01)
    staff_recs_img = img.copy()
    for r in staff_recs:
        r.draw(staff_recs_img, (0, 0, 255), 2)
    cv2.imwrite('staff_recs_img.png', staff_recs_img)
    open_file('staff_recs_img.png')

    print("-------------------------------------------")
    # print(5/0)

    print("Discovering staff locations...")
    staff_boxes = merge_recs([Rectangle(0, r.y, img_width, r.h)
                             for r in staff_recs], 0.01)
    staff_boxes_img = img.copy()
    for r in staff_boxes:
        r.draw(staff_boxes_img, (0, 0, 255), 2)
    cv2.imwrite('staff_boxes_img.png', staff_boxes_img)
    open_file('staff_boxes_img.png')

    print("Matching sharp image...")
    sharp_recs = locate_images(
        img_gray,
        sharp_imgs,
        sharp_lower,
        sharp_upper,
        sharp_thresh)

    print("Merging sharp image results...")
    sharp_recs = merge_recs([j for i in sharp_recs for j in i], 0.5)
    sharp_recs_img = img.copy()
    for r in sharp_recs:
        r.draw(sharp_recs_img, (0, 0, 255), 2)
    cv2.imwrite('sharp_recs_img.png', sharp_recs_img)
    open_file('sharp_recs_img.png')

    print("Matching flat image...")
    flat_recs = locate_images(
        img_gray,
        flat_imgs,
        flat_lower,
        flat_upper,
        flat_thresh)

    print("Merging flat image results...")
    flat_recs = merge_recs([j for i in flat_recs for j in i], 0.5)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(flat_recs_img, (0, 0, 255), 2)
    cv2.imwrite('flat_recs_img.png', flat_recs_img)
    open_file('flat_recs_img.png')

    print("Matching quarter image...")
    quarter_recs = locate_images(
        img_gray,
        quarter_imgs,
        quarter_lower,
        quarter_upper,
        quarter_thresh)

    print("Merging quarter image results...")
    quarter_recs = merge_recs([j for i in quarter_recs for j in i], 0.5)
    quarter_recs_img = img.copy()
    for r in quarter_recs:
        r.draw(quarter_recs_img, (0, 0, 255), 2)
    cv2.imwrite('quarter_recs_img.png', quarter_recs_img)
    open_file('quarter_recs_img.png')

    print("Matching half image...")
    half_recs = locate_images(
        img_gray,
        half_imgs,
        half_lower,
        half_upper,
        half_thresh)

    print("Merging half image results...")
    half_recs = merge_recs([j for i in half_recs for j in i], 0.5)
    half_recs_img = img.copy()
    for r in half_recs:
        r.draw(half_recs_img, (0, 0, 255), 2)
    cv2.imwrite('half_recs_img.png', half_recs_img)
    open_file('half_recs_img.png')

    print("Matching whole image...")
    whole_recs = locate_images(
        img_gray,
        whole_imgs,
        whole_lower,
        whole_upper,
        whole_thresh)

    print("Merging whole image results...")
    whole_recs = merge_recs([j for i in whole_recs for j in i], 0.5)
    whole_recs_img = img.copy()
    for r in whole_recs:
        r.draw(whole_recs_img, (0, 0, 255), 2)
    cv2.imwrite('whole_recs_img.png', whole_recs_img)
    open_file('whole_recs_img.png')

    note_groups = []
    for box in staff_boxes:
        staff_sharps = [
            Note(
                r,
                "sharp",
                box) for r in sharp_recs if abs(
                r.middle[1] -
                box.middle[1]) < box.h *
            5.0 /
            8.0]
        staff_flats = [
            Note(
                r,
                "flat",
                box) for r in flat_recs if abs(
                r.middle[1] -
                box.middle[1]) < box.h *
            5.0 /
            8.0]
        quarter_notes = [
            Note(
                r,
                "4,8",
                box,
                staff_sharps,
                staff_flats) for r in quarter_recs if abs(
                r.middle[1] -
                box.middle[1]) < box.h *
            5.0 /
            8.0]
        half_notes = [
            Note(
                r,
                "2",
                box,
                staff_sharps,
                staff_flats) for r in half_recs if abs(
                r.middle[1] -
                box.middle[1]) < box.h *
            5.0 /
            8.0]
        whole_notes = [
            Note(
                r,
                "1",
                box,
                staff_sharps,
                staff_flats) for r in whole_recs if abs(
                r.middle[1] -
                box.middle[1]) < box.h *
            5.0 /
            8.0]
        staff_notes = quarter_notes + half_notes + whole_notes
        staff_notes.sort(key=lambda n: n.rec.x)
        staffs = [r for r in staff_recs if r.overlap(box) > 0]
        staffs.sort(key=lambda r: r.x)
        note_color = (randint(0, 255), randint(0, 255), randint(0, 255))
        note_group = []
        i = 0
        j = 0
        while i < len(staff_notes):
            if staff_notes[i].rec.x > staffs[j].x and j < len(staffs):
                r = staffs[j]
                j += 1
                if len(note_group) > 0:
                    note_groups.append(note_group)
                    note_group = []
                note_color = (
                    randint(
                        0, 255), randint(
                        0, 255), randint(
                        0, 255))
            else:
                note_group.append(staff_notes[i])
                staff_notes[i].rec.draw(img, note_color, 2)
                i += 1
        note_groups.append(note_group)

    for r in staff_boxes:
        r.draw(img, (0, 0, 255), 2)
    for r in sharp_recs:
        r.draw(img, (0, 0, 255), 2)
    flat_recs_img = img.copy()
    for r in flat_recs:
        r.draw(img, (0, 0, 255), 2)

    cv2.imwrite('res.png', img)
    open_file('res.png')

    for note_group in note_groups:
        print([note.note + " " + note.sym for note in note_group])

    midi = MIDIFile(1)

    track = 0
    time = 0
    channel = 0
    volume = 100

    midi.addTrackName(track, time, "Track")
    midi.addTempo(track, time, 140)

    for note_group in note_groups:
        duration = None
        for note in note_group:
            note_type = note.sym
            if note_type == "1":
                duration = 4
            elif note_type == "2":
                duration = 2
            elif note_type == "4,8":
                duration = 1 if len(note_group) == 1 else 0.5
            pitch = note.pitch
            midi.addNote(track, channel, pitch, time, duration, volume)
            time += duration

    midi.addNote(track, channel, pitch, time, 4, 0)
    # And write it to disk.
    binfile = open("output.mid", 'wb')
    midi.writeFile(binfile)
    binfile.close()
    open_file('output.mid')
