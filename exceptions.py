class ArchiveError(Exception):
    """Base class for exceptions."""

    def __init__(self, *args):
        super().__init__(*args)


# def raiseFunc(in_value: list[bool, str]) -> None:
#     if in_value[0]:
#         pass
#     else:
#         if in_value[1] == "formatError":
#             raise FormatError
#         elif in_value[1] == "itemGone":
#             raise MissingContentError


class FormatError(ArchiveError):  # 想要例如png时，给定文件为.py
    pass


class MissingContentError(ArchiveError):  # 需要20个文件，少了
    pass


class NotLoadedError(ArchiveError):  # 尝试在未设定路径时加载
    pass


class InformationGone(ArchiveError):  # #号头标缺失
    pass


class PictureNotExist(ArchiveError):  # 图片is None
    pass
