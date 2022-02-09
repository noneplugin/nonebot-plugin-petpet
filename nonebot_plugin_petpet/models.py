from PIL import Image
from PIL.Image import Image as IMG


class UserInfo:
    def __init__(self, qq: str = "", group: str = "", img_url: str = ""):
        self.qq: str = qq
        self.group: str = group
        self.name: str = ""
        self.gender: str = ""  # male 或 female 或 unknown
        self.img_url: str = img_url
        self.img: IMG = Image.new("RGBA", (640, 640))
