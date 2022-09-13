from ._main import *


class SheetVisionLib:
    def __init__(self):
        self.pic_path = {}

    def pictures_path_load(self, value: dict) -> bool:
        for i in ["staff_files", "quarter_files", "sharp_files", "flat_files", "half_files", "whole_files"]:
            if i in value.keys():
                for j in value[i]:
                    if j[j.__len__() - 3:] not in ["jpg", "png", "gif", "pmb"]:
                        return False
                    else:
                        pass
            else:
                return False
        self.pic_path = value
        print(self.pic_path)
        return True

    def pictures_reload(self):
        pass

    def pictures_data_load(self):
        pass

    def pictures_locating(self):
        pass

    def merge_rectangles(self):
        pass

    def show_pic(self):
        pass

    def pictures_initialize(self):
        pass

    def sample_match(self):
        pass

    def analysis(self):
        pass

    def midi_dump(self):
        pass
