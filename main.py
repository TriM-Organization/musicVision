# import sheetVisionLib.use_functions
from sheetVisionLib import use_functions
import constants
from bgArrayLogger import *

logger.info("program start")

func_ = use_functions.SheetVisionLib()
func_.pictures_path_load(constants.pictures_path)
func_.pictures_reload()

func_.pictures_data_load(func_.abbreviation_expansion(constants.pictures_data))

# func_.pictures_initialize("./sheetVisionLib/inImg/s2-1.png")
func_.pictures_initialize("./sheetVisionLib/inImg/test0.png")
# func_.pictures_initialize("./sheetVisionLib/inImg/s3.png")

func_.max_min_rectangles()
print(0/0)

func_.base_match()

func_.sample_match(("升记号", "sharp"))  #
