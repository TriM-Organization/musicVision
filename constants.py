pictures_path = {
                 "staff_files": [
                     "./sheetVisionLib/resources/template/staff2.png",
                     "./sheetVisionLib/resources/template/staff.png"],
                 "quarter_files": [
                     "./sheetVisionLib/resources/template/quarter.png",
                     "./sheetVisionLib/resources/template/solid-note.png"],
                 "sharp_files": [
                     "./sheetVisionLib/resources/template/sharp.png"],
                 "flat_files": [
                     "./sheetVisionLib/resources/template/flat-line.png",
                     "./sheetVisionLib/resources/template/flat-space.png"],
                 "half_files": [
                     "./sheetVisionLib/resources/template/half-space.png",
                     "./sheetVisionLib/resources/template/half-note-line.png",
                     "./sheetVisionLib/resources/template/half-line.png",
                     "./sheetVisionLib/resources/template/half-note-space.png"],
                 "whole_files": [
                     "./sheetVisionLib/resources/template/whole-space.png",
                     "./sheetVisionLib/resources/template/whole-note-line.png",
                     "./sheetVisionLib/resources/template/whole-line.png",
                     "./sheetVisionLib/resources/template/whole-note-space.png"]
                 }


staff_lower, staff_upper, staff_thresh = 50, 150, 0.77
sharp_lower, sharp_upper, sharp_thresh = 50, 150, 0.70
flat_lower, flat_upper, flat_thresh = 50, 150, 0.77
quarter_lower, quarter_upper, quarter_thresh = 50, 150, 0.70
half_lower, half_upper, half_thresh = 50, 150, 0.70
whole_lower, whole_upper, whole_thresh = 50, 150, 0.70

pictures_data = {
    "#": ["lower", "upper", "thresh"],
    "staff": [50, 150, 0.77],
    "sharp": [50, 150, 0.70],
    "flat": [50, 150, 0.77],
    "quarter": [50, 150, 0.70],
    "half": [50, 150, 0.70],
    "whole": [50, 150, 0.70]
}
