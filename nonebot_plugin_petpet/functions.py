import random
from datetime import datetime
from collections import namedtuple
from PIL import Image, ImageFilter, ImageDraw
from PIL.Image import Image as IMG
from typing import List, Dict, Optional

from nonebot_plugin_imageutils.fonts import Font
from nonebot_plugin_imageutils import BuildImage, Text2Image

from .download import load_image
from .utils import UserInfo, save_gif, make_jpg_or_gif, translate
from .depends import *


TEXT_TOO_LONG = "文字太长了哦，改短点再试吧~"
NAME_TOO_LONG = "名字太长了哦，改短点再试吧~"
REQUIRE_NAME = "找不到名字，加上名字再试吧~"
REQUIRE_ARG = "该表情至少需要一个参数"


def universal(img: BuildImage = UserImg(), args: List[str] = Args(0, 10)):
    if not args:
        args = ["在此处添加文字"]

    def make(img: BuildImage) -> BuildImage:
        img = img.resize_width(500)
        frames: List[BuildImage] = [img]
        for arg in args:
            text_img = BuildImage(
                Text2Image.from_bbcode_text(arg, fontsize=45, align="center")
                .wrap(480)
                .to_image()
            )
            frames.append(text_img.resize_canvas((500, text_img.height)))

        frame = BuildImage.new(
            "RGBA", (500, sum((f.height for f in frames)) + 10), "white"
        )
        current_h = 0
        for f in frames:
            frame.paste(f, (0, current_h), alpha=True)
            current_h += f.height
        return frame

    return make_jpg_or_gif(img, make)


def petpet(img: BuildImage = UserImg(), arg: str = Arg(["圆"])):
    img = img.convert("RGBA").square()
    if arg == "圆":
        img = img.circle()

    frames: List[IMG] = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    for i in range(5):
        hand = load_image(f"petpet/{i}.png")
        frame = BuildImage.new("RGBA", hand.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frame.paste(hand, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


def kiss(
    user_imgs: List[BuildImage] = UserImgs(1, 2),
    sender_img: BuildImage = SenderImg(),
    arg=NoArg(),
):
    if len(user_imgs) >= 2:
        self_img = user_imgs[0]
        user_img = user_imgs[1]
    else:
        self_img = sender_img
        user_img = user_imgs[0]
    self_head = self_img.convert("RGBA").circle().resize((40, 40))
    user_head = user_img.convert("RGBA").circle().resize((50, 50))
    # fmt: off
    user_locs = [
        (58, 90), (62, 95), (42, 100), (50, 100), (56, 100), (18, 120), (28, 110),
        (54, 100), (46, 100), (60, 100), (35, 115), (20, 120), (40, 96)
    ]
    self_locs = [
        (92, 64), (135, 40), (84, 105), (80, 110), (155, 82), (60, 96), (50, 80),
        (98, 55), (35, 65), (38, 100), (70, 80), (84, 65), (75, 65)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(13):
        frame = load_image(f"kiss/{i}.png")
        frame.paste(user_head, user_locs[i], alpha=True)
        frame.paste(self_head, self_locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def rub(
    user_imgs: List[BuildImage] = UserImgs(1, 2),
    sender_img: BuildImage = SenderImg(),
    arg=NoArg(),
):
    if len(user_imgs) >= 2:
        self_img = user_imgs[0]
        user_img = user_imgs[1]
    else:
        self_img = sender_img
        user_img = user_imgs[0]
    self_head = self_img.convert("RGBA").circle()
    user_head = user_img.convert("RGBA").circle()
    # fmt: off
    user_locs = [
        (39, 91, 75, 75), (49, 101, 75, 75), (67, 98, 75, 75),
        (55, 86, 75, 75), (61, 109, 75, 75), (65, 101, 75, 75)
    ]
    self_locs = [
        (102, 95, 70, 80, 0), (108, 60, 50, 100, 0), (97, 18, 65, 95, 0),
        (65, 5, 75, 75, -20), (95, 57, 100, 55, -70), (109, 107, 65, 75, 0)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(6):
        frame = load_image(f"rub/{i}.png")
        x, y, w, h = user_locs[i]
        frame.paste(user_head.resize((w, h)), (x, y), alpha=True)
        x, y, w, h, angle = self_locs[i]
        frame.paste(
            self_head.resize((w, h)).rotate(angle, expand=True), (x, y), alpha=True
        )
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def play(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [
        (180, 60, 100, 100), (184, 75, 100, 100), (183, 98, 100, 100),
        (179, 118, 110, 100), (156, 194, 150, 48), (178, 136, 122, 69),
        (175, 66, 122, 85), (170, 42, 130, 96), (175, 34, 118, 95),
        (179, 35, 110, 93), (180, 54, 102, 93), (183, 58, 97, 92),
        (174, 35, 120, 94), (179, 35, 109, 93), (181, 54, 101, 92),
        (182, 59, 98, 92), (183, 71, 90, 96), (180, 131, 92, 101)
    ]
    # fmt: on
    raw_frames: List[BuildImage] = [load_image(f"play/{i}.png") for i in range(23)]
    img_frames: List[BuildImage] = []
    for i in range(len(locs)):
        frame = raw_frames[i]
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        img_frames.append(frame)
    frames = (
        img_frames[0:12]
        + img_frames[0:12]
        + img_frames[0:8]
        + img_frames[12:18]
        + raw_frames[18:23]
    )
    frames = [frame.image for frame in frames]
    return save_gif(frames, 0.06)


def pat(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    locs = [(11, 73, 106, 100), (8, 79, 112, 96)]
    img_frames: List[IMG] = []
    for i in range(10):
        frame = load_image(f"pat/{i}.png")
        x, y, w, h = locs[1] if i == 2 else locs[0]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        img_frames.append(frame.image)
    # fmt: off
    seq = [0, 1, 2, 3, 1, 2, 3, 0, 1, 2, 3, 0, 0, 1, 2, 3, 0, 0, 0, 0, 4, 5, 5, 5, 6, 7, 8, 9]
    # fmt: on
    frames = [img_frames[n] for n in seq]
    return save_gif(frames, 0.085)


def rip(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((385, 385))
    frame = load_image("rip/0.png")
    frame.paste(img.rotate(24, expand=True), (-5, 355), below=True)
    frame.paste(img.rotate(-11, expand=True), (649, 310), below=True)
    return frame.save_jpg()


def throw(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").circle().rotate(random.randint(1, 360)).resize((143, 143))
    frame = load_image("throw/0.png")
    frame.paste(img, (15, 178), alpha=True)
    return frame.save_jpg()


def throw_gif(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").circle()
    locs = [
        [(32, 32, 108, 36)],
        [(32, 32, 122, 36)],
        [],
        [(123, 123, 19, 129)],
        [(185, 185, -50, 200), (33, 33, 289, 70)],
        [(32, 32, 280, 73)],
        [(35, 35, 259, 31)],
        [(175, 175, -50, 220)],
    ]
    frames: List[IMG] = []
    for i in range(8):
        frame = load_image(f"throw_gif/{i}.png")
        for w, h, x, y in locs[i]:
            frame.paste(img.resize((w, h)), (x, y), alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def crawl(img: BuildImage = UserImg(), arg: str = Arg()):
    num = 0
    total_num = 92
    if arg.isdigit() and 1 <= int(arg) <= total_num:
        num = int(arg)
    else:
        num = random.randint(1, total_num)

    img = img.convert("RGBA").circle().resize((100, 100))
    frame = load_image(f"crawl/{num:02d}.jpg")
    frame.paste(img, (0, 400), alpha=True)
    return frame.save_jpg()


def support(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((815, 815)).rotate(23, expand=True)
    frame = load_image("support/0.png")
    frame.paste(img, (-172, -17), below=True)
    return frame.save_jpg()


def always(img: BuildImage = UserImg(), arg=NoArg()):
    def make(img: BuildImage) -> BuildImage:
        img_big = img.resize_width(500)
        img_small = img.resize_width(100)
        h1 = img_big.height
        h2 = max(img_small.height, 80)
        frame = BuildImage.new("RGBA", (500, h1 + h2 + 10), "white")
        frame.paste(img_big, alpha=True).paste(
            img_small, (290, h1 + 5 + (h2 - img_small.height) // 2), alpha=True
        )
        frame.draw_text(
            (20, h1 + 5, 280, h1 + h2 + 5), "要我一直", halign="right", max_fontsize=60
        )
        frame.draw_text(
            (400, h1 + 5, 480, h1 + h2 + 5), "吗", halign="left", max_fontsize=60
        )
        return frame

    return make_jpg_or_gif(img, make)


def loading(img: BuildImage = UserImg(), arg=NoArg()):
    img_big = img.convert("RGBA").resize_width(500)
    img_big = img_big.filter(ImageFilter.GaussianBlur(radius=3))
    h1 = img_big.height
    mask = BuildImage.new("RGBA", img_big.size, (0, 0, 0, 64))
    icon = load_image("loading/icon.png")
    img_big.paste(mask, alpha=True).paste(icon, (200, int(h1 / 2) - 50), alpha=True)

    def make(img: BuildImage) -> BuildImage:
        img_small = img.resize_width(100)
        h2 = max(img_small.height, 80)
        frame = BuildImage.new("RGBA", (500, h1 + h2 + 10), "white")
        frame.paste(img_big, alpha=True).paste(
            img_small, (100, h1 + 5 + (h2 - img_small.height) // 2), alpha=True
        )
        frame.draw_text(
            (210, h1 + 5, 480, h1 + h2 + 5), "不出来", halign="left", max_fontsize=60
        )
        return frame

    return make_jpg_or_gif(img, make)


def turn(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").circle()
    frames: List[IMG] = []
    for i in range(0, 360, 10):
        frame = BuildImage.new("RGBA", (250, 250), "white")
        frame.paste(img.rotate(i).resize((250, 250)), alpha=True)
        frames.append(frame.image)
    if random.randint(0, 1):
        frames.reverse()
    return save_gif(frames, 0.05)


def littleangel(user: UserInfo = User(), arg: str = Arg()):
    img = user.img.convert("RGBA").resize_width(500)
    img_w, img_h = img.size
    frame = BuildImage.new("RGBA", (600, img_h + 230), "white")
    frame.paste(img, (int(300 - img_w / 2), 110), alpha=True)

    text = "非常可爱！简直就是小天使"
    frame.draw_text(
        (10, img_h + 120, 590, img_h + 185), text, max_fontsize=48, weight="bold"
    )

    ta = "他" if user.gender == "male" else "她"
    text = f"{ta}没失踪也没怎么样  我只是觉得你们都该看一下"
    frame.draw_text(
        (20, img_h + 180, 580, img_h + 215), text, max_fontsize=26, weight="bold"
    )

    name = arg or user.name or ta
    text = f"请问你们看到{name}了吗?"
    try:
        frame.draw_text(
            (20, 0, 580, 110), text, max_fontsize=70, min_fontsize=25, weight="bold"
        )
    except ValueError:
        return NAME_TOO_LONG

    return frame.save_jpg()


def dont_touch(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((170, 170))
    frame = load_image("dont_touch/0.png")
    frame.paste(img, (23, 231), alpha=True)
    return frame.save_jpg()


def alike(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((90, 90))
    frame = load_image("alike/0.png")
    frame.paste(img, (131, 14), alpha=True)
    return frame.save_jpg()


def roll(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((210, 210))
    # fmt: off
    locs = [
        (87, 77, 0), (96, 85, -45), (92, 79, -90), (92, 78, -135),
        (92, 75, -180), (92, 75, -225), (93, 76, -270), (90, 80, -315)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(8):
        frame = load_image(f"roll/{i}.png")
        x, y, a = locs[i]
        frame.paste(img.rotate(a), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def play_game(img: BuildImage = UserImg(), arg: str = Arg()):
    text = arg or "来玩休闲游戏啊"
    frame = load_image("play_game/0.png")
    try:
        frame.draw_text(
            (20, frame.height - 70, frame.width - 20, frame.height),
            text,
            max_fontsize=40,
            min_fontsize=25,
            stroke_fill="white",
            stroke_ratio=0.06,
        )
    except:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        points = ((0, 5), (227, 0), (216, 150), (0, 165))
        screen = img.resize((220, 160), keep_ratio=True).perspective(points)
        return frame.copy().paste(screen.rotate(9, expand=True), (161, 117), below=True)

    return make_jpg_or_gif(img, make)


def worship(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA")
    points = ((0, -30), (135, 17), (135, 145), (0, 140))
    paint = img.square().resize((150, 150)).perspective(points)
    frames: List[IMG] = []
    for i in range(10):
        frame = load_image(f"worship/{i}.png")
        frame.paste(paint, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


def eat(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((32, 32))
    frames = []
    for i in range(3):
        frame = load_image(f"eat/{i}.png")
        frame.paste(img, (1, 38), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def bite(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    frames: List[IMG] = []
    # fmt: off
    locs = [
        (90, 90, 105, 150), (90, 83, 96, 172), (90, 90, 106, 148),
        (88, 88, 97, 167), (90, 85, 89, 179), (90, 90, 106, 151)
    ]
    # fmt: on
    for i in range(6):
        frame = load_image(f"bite/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    for i in range(6, 16):
        frame = load_image(f"bite/{i}.png")
        frames.append(frame.image)
    return save_gif(frames, 0.07)


def police(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((245, 245))
    frame = load_image("police/0.png")
    frame.paste(img, (224, 46), below=True)
    return frame.save_jpg()


def police1(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((60, 75), keep_ratio=True).rotate(16, expand=True)
    frame = load_image("police/1.png")
    frame.paste(img, (37, 291), below=True)
    return frame.save_jpg()


def ask(user: UserInfo = User(), arg: str = Arg()):
    img = user.img.resize_width(640)
    img_w, img_h = img.size
    gradient_h = 150
    gradient = BuildImage.new("RGBA", (img_w, gradient_h)).gradient_color(
        (0, 0, 0, 220), (0, 0, 0, 30)
    )
    mask = BuildImage.new("RGBA", img.size)
    mask.paste(gradient, (0, img_h - gradient_h), alpha=True)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
    img.paste(mask, alpha=True)

    name = arg or user.name
    ta = "他" if user.gender == "male" else "她"
    if not name:
        return REQUIRE_NAME

    start_w = 20
    start_h = img_h - gradient_h + 5
    text_img1 = Text2Image.from_text(
        f"{name}", 28, fill="orange", weight="bold"
    ).to_image()
    text_img2 = Text2Image.from_text(
        f"{name}不知道哦。", 28, fill="white", weight="bold"
    ).to_image()
    img.paste(
        text_img1,
        (start_w + 40 + (text_img2.width - text_img1.width) // 2, start_h),
        alpha=True,
    )
    img.paste(
        text_img2,
        (start_w + 40, start_h + text_img1.height + 10),
        alpha=True,
    )

    line_h = start_h + text_img1.height + 5
    img.draw_line(
        (start_w, line_h, start_w + text_img2.width + 80, line_h),
        fill="orange",
        width=2,
    )

    sep_w = 30
    sep_h = 80
    frame = BuildImage.new("RGBA", (img_w + sep_w * 2, img_h + sep_h * 2), "white")
    try:
        frame.draw_text(
            (sep_w, 0, img_w + sep_w, sep_h),
            f"让{name}告诉你吧",
            max_fontsize=35,
            halign="left",
        )
        frame.draw_text(
            (sep_w, img_h + sep_h, img_w + sep_w, img_h + sep_h * 2),
            f"啊这，{ta}说不知道",
            max_fontsize=35,
            halign="left",
        )
    except ValueError:
        return NAME_TOO_LONG
    frame.paste(img, (sep_w, sep_h))
    return frame.save_jpg()


def prpr(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("prpr/0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((0, 19), (236, 0), (287, 264), (66, 351))
        screen = img.resize((330, 330), keep_ratio=True).perspective(points)
        return frame.copy().paste(screen, (56, 284), below=True)

    return make_jpg_or_gif(img, make)


def twist(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (25, 66, 0), (25, 66, 60), (23, 68, 120),
        (20, 69, 180), (22, 68, 240), (25, 66, 300)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(5):
        frame = load_image(f"twist/{i}.png")
        x, y, a = locs[i]
        frame.paste(img.rotate(a), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def wallpaper(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("wallpaper/0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((775, 496), keep_ratio=True), (260, 580), below=True
        )

    return make_jpg_or_gif(img, make, gif_zoom=0.5)


def china_flag(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("china_flag/0.png")
    frame.paste(img.convert("RGBA").resize(frame.size, keep_ratio=True), below=True)
    return frame.save_jpg()


def make_friend(user: UserInfo = User(), arg: str = Arg()):
    img = user.img.convert("RGBA")

    bg = load_image("make_friend/0.png")
    frame = img.resize_width(1000)
    frame.paste(
        img.resize_width(250).rotate(9, expand=True),
        (743, frame.height - 155),
        alpha=True,
    )
    frame.paste(
        img.square().resize((55, 55)).rotate(9, expand=True),
        (836, frame.height - 278),
        alpha=True,
    )
    frame.paste(bg, (0, frame.height - 1000), alpha=True)

    name = arg or user.name
    if not name:
        return REQUIRE_NAME

    text_img = Text2Image.from_text(name, 20, fill="white").to_image()
    if text_img.width > 230:
        return NAME_TOO_LONG

    text_img = BuildImage(text_img).rotate(9, expand=True)
    frame.paste(text_img, (710, frame.height - 308), alpha=True)
    return frame.save_jpg()


def back_to_work(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("back_to_work/0.png")
    img = img.convert("RGBA").resize((220, 310), keep_ratio=True, direction="north")
    frame.paste(img.rotate(25, expand=True), (56, 32), below=True)
    return frame.save_jpg()


def perfect(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("perfect/0.png")
    img = img.convert("RGBA").resize((310, 460), keep_ratio=True, inside=True)
    frame.paste(img, (313, 64), alpha=True)
    return frame.save_jpg()


def follow(user: UserInfo = User(), arg: str = Arg()):
    img = user.img.circle().resize((200, 200))

    ta = "女同" if user.gender == "female" else "男同"
    name = arg or user.name or ta
    name_img = Text2Image.from_text(name, 60).to_image()
    follow_img = Text2Image.from_text("关注了你", 60, fill="grey").to_image()
    text_width = max(name_img.width, follow_img.width)
    if text_width >= 1000:
        return NAME_TOO_LONG

    frame = BuildImage.new("RGBA", (300 + text_width + 50, 300), (255, 255, 255, 0))
    frame.paste(img, (50, 50), alpha=True)
    frame.paste(name_img, (300, 135 - name_img.height), alpha=True)
    frame.paste(follow_img, (300, 145), alpha=True)
    return frame.save_jpg()


def my_friend(
    user: Optional[UserInfo] = User(),
    sender: UserInfo = Sender(),
    name: str = RegexArg("name"),
    args: List[str] = Args(0, 10),
):
    if not user:
        user = sender
    if not args:
        return REQUIRE_ARG
    name = name.strip() or user.name or "朋友"
    texts = args
    img = user.img.convert("RGBA").circle().resize((100, 100))

    name_img = Text2Image.from_text(name, 25, fill="#868894").to_image()
    name_w, name_h = name_img.size
    if name_w >= 600:
        raise ValueError(NAME_TOO_LONG)

    corner1 = load_image("my_friend/corner1.png")
    corner2 = load_image("my_friend/corner2.png")
    corner3 = load_image("my_friend/corner3.png")
    corner4 = load_image("my_friend/corner4.png")
    label = load_image("my_friend/label.png")

    def make_dialog(text: str) -> BuildImage:
        text_img = Text2Image.from_text(text, 40).wrap(600).to_image()
        text_w, text_h = text_img.size
        box_w = max(text_w, name_w + 15) + 140
        box_h = max(text_h + 103, 150)
        box = BuildImage.new("RGBA", (box_w, box_h))
        box.paste(corner1, (0, 0))
        box.paste(corner2, (0, box_h - 75))
        box.paste(corner3, (text_w + 70, 0))
        box.paste(corner4, (text_w + 70, box_h - 75))
        box.paste(BuildImage.new("RGBA", (text_w, box_h - 40), "white"), (70, 20))
        box.paste(BuildImage.new("RGBA", (text_w + 88, box_h - 150), "white"), (27, 75))
        box.paste(text_img, (70, 17 + (box_h - 40 - text_h) // 2), alpha=True)

        dialog = BuildImage.new("RGBA", (box.width + 130, box.height + 60), "#eaedf4")
        dialog.paste(img, (20, 20), alpha=True)
        dialog.paste(box, (130, 60), alpha=True)
        dialog.paste(label, (160, 25))
        dialog.paste(name_img, (260, 22 + (35 - name_h) // 2), alpha=True)
        return dialog

    dialogs = [make_dialog(text) for text in texts]
    frame_w = max((dialog.width for dialog in dialogs))
    frame_h = sum((dialog.height for dialog in dialogs))
    frame = BuildImage.new("RGBA", (frame_w, frame_h), "#eaedf4")
    current_h = 0
    for dialog in dialogs:
        frame.paste(dialog, (0, current_h))
        current_h += dialog.height
    return frame.save_jpg()


def paint(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((117, 135), keep_ratio=True)
    frame = load_image("paint/0.png")
    frame.paste(img.rotate(4, expand=True), (95, 107), below=True)
    return frame.save_jpg()


def shock(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((300, 300))
    frames: List[IMG] = []
    for i in range(30):
        frames.append(
            img.motion_blur(random.randint(-90, 90), random.randint(0, 50))
            .rotate(random.randint(-20, 20))
            .image
        )
    return save_gif(frames, 0.01)


def coupon(user: UserInfo = User(), arg: str = Arg()):
    text = (arg or f"{user.name}陪睡券") + "\n（永久有效）"
    text_img = BuildImage.new("RGBA", (250, 100))
    try:
        text_img.draw_text(
            (0, 0, text_img.width, text_img.height),
            text,
            lines_align="center",
            max_fontsize=30,
            min_fontsize=15,
        )
    except ValueError:
        return TEXT_TOO_LONG

    frame = load_image("coupon/0.png")
    img = user.img.convert("RGBA").circle().resize((60, 60)).rotate(22, expand=True)
    frame.paste(img, (164, 85), alpha=True)
    frame.paste(text_img.rotate(22, expand=True), (94, 108), alpha=True)
    return frame.save_jpg()


def listen_music(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA")
    frame = load_image("listen_music/0.png")
    frames: List[IMG] = []
    for i in range(0, 360, 10):
        frames.append(
            frame.copy()
            .paste(img.rotate(-i).resize((215, 215)), (100, 100), below=True)
            .image
        )
    return save_gif(frames, 0.05)


async def dianzhongdian(img: BuildImage = UserImg(), arg: str = Arg()):
    if not arg:
        return REQUIRE_ARG

    trans = await translate(arg)
    img = img.convert("L").resize_width(500)
    text_img1 = BuildImage.new("RGBA", (500, 60))
    text_img2 = BuildImage.new("RGBA", (500, 35))
    try:
        text_img1.draw_text(
            (20, 0, text_img1.width - 20, text_img1.height),
            arg,
            max_fontsize=50,
            min_fontsize=25,
            fill="white",
        )
        text_img2.draw_text(
            (20, 0, text_img2.width - 20, text_img2.height),
            trans,
            max_fontsize=25,
            min_fontsize=10,
            fill="white",
        )
    except ValueError:
        return TEXT_TOO_LONG

    frame = BuildImage.new("RGBA", (500, img.height + 100), "black")
    frame.paste(img, alpha=True)
    frame.paste(text_img1, (0, img.height), alpha=True)
    frame.paste(text_img2, (0, img.height + 60), alpha=True)
    return frame.save_jpg()


def funny_mirror(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((500, 500))
    frames: List[IMG] = [img.image]
    coeffs = [0.01, 0.03, 0.05, 0.08, 0.12, 0.17, 0.23, 0.3, 0.4, 0.6]
    borders = [25, 52, 67, 83, 97, 108, 118, 128, 138, 148]
    for i in range(10):
        new_size = 500 - borders[i] * 2
        new_img = img.distort((coeffs[i], 0, 0, 0)).resize_canvas((new_size, new_size))
        frames.append(new_img.resize((500, 500)).image)
    frames.extend(frames[::-1])
    return save_gif(frames, 0.05)


def love_you(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    frames: List[IMG] = []
    locs = [(68, 65, 70, 70), (63, 59, 80, 80)]
    for i in range(2):
        heart = load_image(f"love_you/{i}.png")
        frame = BuildImage.new("RGBA", heart.size, "white")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True).paste(heart, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


def symmetric(img: BuildImage = UserImg(), arg: str = Arg(["上", "下", "左", "右"])):
    img = img.convert("RGBA").resize_width(500)
    img_w, img_h = img.size

    Mode = namedtuple(
        "Mode", ["method", "frame_size", "size1", "pos1", "size2", "pos2"]
    )
    modes: Dict[str, Mode] = {
        "left": Mode(
            Image.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (0, 0, img_w // 2, img_h),
            (0, 0),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
        ),
        "right": Mode(
            Image.FLIP_LEFT_RIGHT,
            (img_w // 2 * 2, img_h),
            (img_w // 2, 0, img_w // 2 * 2, img_h),
            (img_w // 2, 0),
            (0, 0, img_w // 2, img_h),
            (0, 0),
        ),
        "top": Mode(
            Image.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
        ),
        "bottom": Mode(
            Image.FLIP_TOP_BOTTOM,
            (img_w, img_h // 2 * 2),
            (0, img_h // 2, img_w, img_h // 2 * 2),
            (0, img_h // 2),
            (0, 0, img_w, img_h // 2),
            (0, 0),
        ),
    }

    mode = modes["left"]
    if arg == "右":
        mode = modes["right"]
    elif arg == "上":
        mode = modes["top"]
    elif arg == "下":
        mode = modes["bottom"]

    first = img
    second = img.transpose(mode.method)
    frame = BuildImage.new("RGBA", mode.frame_size)
    frame.paste(first.crop(mode.size1), mode.pos1)
    frame.paste(second.crop(mode.size2), mode.pos2)
    return frame.save_jpg()


def safe_sense(user: UserInfo = User(), arg: str = Arg()):
    img = user.img.convert("RGBA").resize((215, 343), keep_ratio=True)
    frame = load_image(f"safe_sense/0.png")
    frame.paste(img, (215, 135))

    ta = "他" if user.gender == "male" else "她"
    text = arg or f"你给我的安全感\n远不及{ta}的万分之一"
    try:
        frame.draw_text(
            (30, 0, 400, 130),
            text,
            max_fontsize=50,
            allow_wrap=True,
            lines_align="center",
        )
    except ValueError:
        return TEXT_TOO_LONG
    return frame.save_jpg()


def always_like(users: List[UserInfo] = Users(1, 6), args: List[str] = Args(0, 6)):
    img = users[0].img.convert("RGBA")
    name = (args[0] if args else "") or users[0].name
    if not name:
        return REQUIRE_NAME
    text = f"我永远喜欢{name}"

    frame = load_image(f"always_like/0.png")
    frame.paste(
        img.resize((350, 400), keep_ratio=True, inside=True), (25, 35), alpha=True
    )
    try:
        frame.draw_text(
            (20, 470, frame.width - 20, 570),
            text,
            max_fontsize=70,
            min_fontsize=30,
            weight="bold",
        )
    except ValueError:
        return NAME_TOO_LONG

    def random_color():
        return random.choice(
            ["red", "darkorange", "gold", "darkgreen", "blue", "cyan", "purple"]
        )

    if len(users) > 1:
        text_w = Text2Image.from_text(text, 70).to_image().width
        ratio = min((frame.width - 40) / text_w, 1)
        text_w *= ratio
        name_w = Text2Image.from_text(name, 70).to_image().width * ratio
        start_w = text_w - name_w + (frame.width - text_w) // 2
        frame.draw_line(
            (start_w, 525, start_w + name_w, 525), fill=random_color(), width=10
        )

    current_h = 400
    for i, user in enumerate(users[1:], start=1):
        img = user.img.convert("RGBA")
        frame.paste(
            img.resize((350, 400), keep_ratio=True, inside=True),
            (10 + random.randint(0, 50), 20 + random.randint(0, 70)),
            alpha=True,
        )
        name = (args[i] if len(args) > i else "") or user.name
        if not name:
            return "找不到对应的名字，名字数须与目标数一致"
        try:
            frame.draw_text(
                (400, current_h, frame.width - 20, current_h + 80),
                name,
                max_fontsize=70,
                min_fontsize=30,
                weight="bold",
            )
        except ValueError:
            return NAME_TOO_LONG

        if len(users) > i + 1:
            name_w = min(Text2Image.from_text(name, 70).to_image().width, 380)
            start_w = 400 + (410 - name_w) // 2
            line_h = current_h + 40
            frame.draw_line(
                (start_w, line_h, start_w + name_w, line_h),
                fill=random_color(),
                width=10,
            )
        current_h -= 70
    return frame.save_jpg()


def interview(imgs: List[BuildImage] = UserImgs(1, 2), arg: str = Arg()):
    if len(imgs) >= 2:
        self_img = imgs[0]
        user_img = imgs[1]
    else:
        self_img = load_image("interview/huaji.png")
        user_img = imgs[0]
    self_img = self_img.convert("RGBA").square().resize((124, 124))
    user_img = user_img.convert("RGBA").square().resize((124, 124))

    frame = BuildImage.new("RGBA", (600, 310), "white")
    microphone = load_image("interview/microphone.png")
    frame.paste(microphone, (330, 103), alpha=True)
    frame.paste(self_img, (419, 40), alpha=True)
    frame.paste(user_img, (57, 40), alpha=True)
    try:
        frame.draw_text(
            (20, 200, 580, 310), arg or "采访大佬经验", max_fontsize=50, min_fontsize=20
        )
    except ValueError:
        return TEXT_TOO_LONG
    return frame.save_jpg()


def punch(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((260, 260))
    frames: List[IMG] = []
    # fmt: off
    locs = [
        (-50, 20), (-40, 10), (-30, 0), (-20, -10), (-10, -10), (0, 0),
        (10, 10), (20, 20), (10, 10), (0, 0), (-10, -10), (10, 0), (-30, 10)
    ]
    # fmt: on
    for i in range(13):
        fist = load_image(f"punch/{i}.png")
        frame = BuildImage.new("RGBA", fist.size, "white")
        x, y = locs[i]
        frame.paste(img, (x, y - 15), alpha=True).paste(fist, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.03)


def cyan(img: BuildImage = UserImg(), arg=NoArg()):
    color = (78, 114, 184)
    frame = img.convert("RGB").square().resize((500, 500)).color_mask(color)
    frame.draw_text(
        (400, 40, 480, 280),
        "群\n青",
        max_fontsize=80,
        weight="bold",
        fill="white",
        stroke_ratio=0.04,
        stroke_fill=color,
    ).draw_text(
        (200, 270, 480, 350),
        "YOASOBI",
        halign="right",
        max_fontsize=40,
        fill="white",
        stroke_ratio=0.06,
        stroke_fill=color,
    )
    return frame.save_jpg()


def pound(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [
        (135, 240, 138, 47), (135, 240, 138, 47), (150, 190, 105, 95), (150, 190, 105, 95),
        (148, 188, 106, 98), (146, 196, 110, 88), (145, 223, 112, 61), (145, 223, 112, 61)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(8):
        frame = load_image(f"pound/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def thump(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [(65, 128, 77, 72), (67, 128, 73, 72), (54, 139, 94, 61), (57, 135, 86, 65)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(4):
        frame = load_image(f"thump/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


def need(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((115, 115))
    frame = load_image("need/0.png")
    frame.paste(img, (327, 232), below=True)
    return frame.save_jpg()


def cover_face(img: BuildImage = UserImg(), arg=NoArg()):
    points = ((15, 15), (448, 0), (445, 456), (0, 465))
    img = img.convert("RGBA").square().resize((450, 450)).perspective(points)
    frame = load_image("cover_face/0.png")
    frame.paste(img, (120, 150), below=True)
    return frame.save_jpg()


def knock(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [(60, 308, 210, 195), (60, 308, 210, 198), (45, 330, 250, 172), (58, 320, 218, 180),
            (60, 310, 215, 193), (40, 320, 250, 285), (48, 308, 226, 192), (51, 301, 223, 200)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(8):
        frame = load_image(f"knock/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


def garbage(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((79, 79))
    # fmt: off
    locs = (
        [] + [(39, 40)] * 3 + [(39, 30)] * 2 + [(39, 32)] * 10
        + [(39, 30), (39, 27), (39, 32), (37, 49), (37, 64),
           (37, 67), (37, 67), (39, 69), (37, 70), (37, 70)]
    )
    # fmt: on
    frames: List[IMG] = []
    for i in range(25):
        frame = load_image(f"garbage/{i}.png")
        frame.paste(img, locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.04)


def whyatme(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((265, 265), keep_ratio=True)
    frame = load_image("whyatme/0.png")
    frame.paste(img, (42, 13), below=True)
    return frame.save_jpg()


def decent_kiss(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((589, 340), keep_ratio=True)
    frame = load_image("decent_kiss/0.png")
    frame.paste(img, (0, 91), below=True)
    return frame.save_jpg()


def jiujiu(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((75, 51), keep_ratio=True)
    frames: List[IMG] = []
    for i in range(8):
        frame = load_image(f"jiujiu/{i}.png")
        frame.paste(img, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


def suck(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [(82, 100, 130, 119), (82, 94, 126, 125), (82, 120, 128, 99), (81, 164, 132, 55),
            (79, 163, 132, 55), (82, 140, 127, 79), (83, 152, 125, 67), (75, 157, 140, 62),
            (72, 165, 144, 54), (80, 132, 128, 87), (81, 127, 127, 92), (79, 111, 132, 108)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(12):
        bg = load_image(f"suck/{i}.png")
        frame = BuildImage.new("RGBA", bg.size, "white")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), alpha=True).paste(bg, alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


def hammer(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    # fmt: off
    locs = [(62, 143, 158, 113), (52, 177, 173, 105), (42, 192, 192, 92), (46, 182, 184, 100),
            (54, 169, 174, 110), (69, 128, 144, 135), (65, 130, 152, 124)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(7):
        frame = load_image(f"hammer/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.07)


def tightly(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((640, 400), keep_ratio=True)
    # fmt: off
    locs = [(39, 169, 267, 141), (40, 167, 264, 143), (38, 174, 270, 135), (40, 167, 264, 143), (38, 174, 270, 135),
            (40, 167, 264, 143), (38, 174, 270, 135), (40, 167, 264, 143), (38, 174, 270, 135), (28, 176, 293, 134),
            (5, 215, 333, 96), (10, 210, 321, 102), (3, 210, 330, 104), (4, 210, 328, 102), (4, 212, 328, 100),
            (4, 212, 328, 100), (4, 212, 328, 100), (4, 212, 328, 100), (4, 212, 328, 100), (29, 195, 285, 120)]
    # fmt: on
    frames: List[IMG] = []
    for i in range(20):
        frame = load_image(f"tightly/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


def distracted(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((500, 500))
    frame = load_image("distracted/1.png")
    label = load_image("distracted/0.png")
    frame.paste(img, below=True).paste(label, (140, 320), alpha=True)
    return frame.save_jpg()


def anyasuki(img: BuildImage = UserImg(), arg: str = Arg()):
    frame = load_image("anyasuki/0.png")
    try:
        frame.draw_text(
            (2, frame.height - 50, frame.width - 20, frame.height),
            arg or "阿尼亚喜欢这个",
            max_fontsize=40,
            fill="white",
            stroke_fill="black",
            stroke_ratio=0.06,
        )
    except ValueError:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((305, 235), keep_ratio=True), (106, 72), below=True
        )

    return make_jpg_or_gif(img, make)


def thinkwhat(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("thinkwhat/0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((534, 493), keep_ratio=True), (530, 0), below=True
        )

    return make_jpg_or_gif(img, make)


def keepaway(imgs: List[BuildImage] = UserImgs(1, 8), arg=NoArg()):
    def trans(img: BuildImage, n: int) -> BuildImage:
        img = img.convert("RGBA").square().resize((100, 100))
        if n < 4:
            return img.rotate(n * 90)
        else:
            return img.transpose(Image.FLIP_LEFT_RIGHT).rotate((n - 4) * 90)

    def paste(img: BuildImage):
        nonlocal count
        y = 90 if count < 4 else 190
        frame.paste(img, ((count % 4) * 100, y))
        count += 1

    frame = BuildImage.new("RGB", (400, 290), "white")
    frame.draw_text(
        (10, 10, 220, 80), "如何提高社交质量 : \n远离以下头像的人", max_fontsize=21, halign="left"
    )
    count = 0
    num_per_user = 8 // len(imgs)
    for img in imgs:
        for n in range(num_per_user):
            paste(trans(img, n))
    num_left = 8 - num_per_user * len(imgs)
    for n in range(num_left):
        paste(trans(imgs[-1], n + num_per_user))

    return frame.save_jpg()


def marriage(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize_height(1080)
    img_w, img_h = img.size
    if img_w > 1500:
        img_w = 1500
    elif img_w < 800:
        img_h = int(img_h * img_w / 800)
    frame = img.resize_canvas((img_w, img_h)).resize_height(1080)
    left = load_image("marriage/0.png")
    right = load_image("marriage/1.png")
    frame.paste(left, alpha=True).paste(
        right, (frame.width - right.width, 0), alpha=True
    )
    return frame.save_jpg()


def painter(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((240, 345), keep_ratio=True, direction="north")
    frame = load_image("painter/0.png")
    frame.paste(img, (125, 91), below=True)
    return frame.save_jpg()


def repeat(
    users: List[UserInfo] = Users(1, 5), sender: UserInfo = Sender(), arg: str = Arg()
):
    def single_msg(user: UserInfo) -> BuildImage:
        user_img = user.img.convert("RGBA").circle().resize((100, 100))
        user_name_img = Text2Image.from_text(f"{user.name}", 40).to_image()
        time = datetime.now().strftime("%H:%M")
        time_img = Text2Image.from_text(time, 40, fill="gray").to_image()
        bg = BuildImage.new("RGB", (1079, 200), (248, 249, 251, 255))
        bg.paste(user_img, (50, 50), alpha=True)
        bg.paste(user_name_img, (175, 45), alpha=True)
        bg.paste(time_img, (200 + user_name_img.width, 50), alpha=True)
        bg.paste(text_img, (175, 100), alpha=True)
        return bg

    text = arg or "救命啊"
    text_img = Text2Image.from_text(text, 50).to_image()
    if text_img.width > 900:
        return TEXT_TOO_LONG

    msg_img = BuildImage.new("RGB", (1079, 1000))
    for i in range(5):
        index = i % len(users)
        msg_img.paste(single_msg(users[index]), (0, 200 * i))
    msg_img_twice = BuildImage.new("RGB", (msg_img.width, msg_img.height * 2))
    msg_img_twice.paste(msg_img).paste(msg_img, (0, msg_img.height))

    input_img = load_image("repeat/0.jpg")
    self_img = sender.img.convert("RGBA").circle().resize((75, 75))
    input_img.paste(self_img, (15, 40), alpha=True)

    frames: List[IMG] = []
    for i in range(50):
        frame = BuildImage.new("RGB", (1079, 1192), "white")
        frame.paste(msg_img_twice, (0, -20 * i))
        frame.paste(input_img, (0, 1000))
        frames.append(frame.image)

    return save_gif(frames, 0.08)


def anti_kidnap(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").circle().resize((450, 450))
    bg = load_image("anti_kidnap/0.png")
    frame = BuildImage.new("RGBA", bg.size, "white")
    frame.paste(img, (30, 78))
    frame.paste(bg, alpha=True)
    return frame.save_jpg()


def charpic(img: BuildImage = UserImg(), arg=NoArg()):
    str_map = "@@$$&B88QMMGW##EE93SPPDOOU**==()+^,\"--''.  "
    num = len(str_map)
    font = Font.find("Consolas").load_font(15)

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("L").resize_width(150)
        img = img.resize((img.width, img.height // 2))
        lines = []
        for y in range(img.height):
            line = ""
            for x in range(img.width):
                gray = img.image.getpixel((x, y))
                line += str_map[int(num * gray / 256)]
            lines.append(line)
        text = "\n".join(lines)
        w, h = font.getsize_multiline(text)
        text_img = Image.new("RGB", (w, h), "white")
        draw = ImageDraw.Draw(text_img)
        draw.multiline_text((0, 0), text, font=font, fill="black")
        return BuildImage(text_img)

    return make_jpg_or_gif(img, make)
