import math
import random
from typing import Dict
from datetime import datetime
from collections import namedtuple
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

from nonebot_plugin_imageutils import Text2Image
from nonebot_plugin_imageutils.fonts import Font
from nonebot_plugin_imageutils.gradient import LinearGradient, ColorStop

from .utils import *
from .depends import *
from .download import load_image

TEXT_TOO_LONG = "文字太长了哦，改短点再试吧~"
NAME_TOO_LONG = "名字太长了哦，改短点再试吧~"
REQUIRE_NAME = "找不到名字，加上名字再试吧~"


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


def capoo_rub(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((180, 180))
    frames: List[IMG] = []
    locs = [
        (178, 184, 78, 260),
        (178, 174, 84, 269),
        (178, 174, 84, 269),
        (178, 178, 84, 264),
    ]
    for i in range(4):
        frame = load_image(f"capoo_rub/{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


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
    raw_frames: List[BuildImage] = [load_image(f"play/{i}.png") for i in range(38)]
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
        + raw_frames[18:38]
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


def rip(user_imgs: List[BuildImage] = UserImgs(1, 2), arg=NoArg()):
    if len(user_imgs) >= 2:
        frame = load_image("rip/1.png")
        self_img = user_imgs[0]
        user_img = user_imgs[1]
    else:
        frame = load_image("rip/0.png")
        self_img = None
        user_img = user_imgs[0]

    user_img = user_img.convert("RGBA").square().resize((385, 385))
    if self_img:
        self_img = self_img.convert("RGBA").square().resize((230, 230))
        frame.paste(self_img, (408, 418), below=True)
    frame.paste(user_img.rotate(24, expand=True), (-5, 355), below=True)
    frame.paste(user_img.rotate(-11, expand=True), (649, 310), below=True)
    return frame.save_jpg()


def rip_angrily(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((105, 105))
    frame = load_image("rip_angrily/0.png")
    frame.paste(img.rotate(-24, expand=True), (18, 170), below=True)
    frame.paste(img.rotate(24, expand=True), (163, 65), below=True)
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


def always_cycle(img: BuildImage = UserImg(), arg=NoArg()):
    tmp = img.convert("RGBA").resize_width(500)
    img_h = tmp.height
    text_h = tmp.resize_width(100).height + tmp.resize_width(20).height + 10
    text_h = max(text_h, 80)
    frame_h = img_h + text_h
    text_frame = BuildImage.new("RGBA", (500, frame_h), "white")
    text_frame.draw_text(
        (0, img_h, 280, frame_h), "要我一直", halign="right", max_fontsize=60
    ).draw_text((400, img_h, 500, frame_h), "吗", halign="left", max_fontsize=60)

    def make(img: BuildImage) -> BuildImage:
        img = img.resize_width(500)
        base_frame = text_frame.copy().paste(img, alpha=True)
        frame = BuildImage.new("RGBA", base_frame.size, "white")
        r = 1
        for _ in range(4):
            x = int(358 * (1 - r))
            y = int(frame_h * (1 - r))
            w = int(500 * r)
            h = int(frame_h * r)
            frame.paste(base_frame.resize((w, h)), (x, y))
            r /= 5
        return frame

    return make_jpg_or_gif(img, make)


def always_always(img: BuildImage = UserImg(), arg=NoArg()):
    tmp = img.convert("RGBA").resize_width(500)
    img_h = tmp.height
    text_h = tmp.resize_width(100).height + tmp.resize_width(20).height + 10
    text_h = max(text_h, 80)
    frame_h = img_h + text_h
    text_frame = BuildImage.new("RGBA", (500, frame_h), "white")
    text_frame.draw_text(
        (0, img_h, 280, frame_h), "要我一直", halign="right", max_fontsize=60
    ).draw_text((400, img_h, 500, frame_h), "吗", halign="left", max_fontsize=60)

    frame_num = 20
    coeff = 5 ** (1 / frame_num)

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.resize_width(500)
            base_frame = text_frame.copy().paste(img, alpha=True)
            frame = BuildImage.new("RGBA", base_frame.size, "white")
            r = coeff**i
            for _ in range(4):
                x = int(358 * (1 - r))
                y = int(frame_h * (1 - r))
                w = int(500 * r)
                h = int(frame_h * r)
                frame.paste(base_frame.resize((w, h)), (x, y))
                r /= 5
            return frame

        return make

    return make_gif_or_combined_gif(
        img, maker, frame_num, 0.1, FrameAlignPolicy.extend_loop
    )


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


def windmill_turn(img: BuildImage = UserImg(), arg=NoArg()):
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA").resize((300, 300), keep_ratio=True)
            frame = BuildImage.new("RGBA", (600, 600), "white")
            frame.paste(img, alpha=True)
            frame.paste(img.rotate(90), (0, 300), alpha=True)
            frame.paste(img.rotate(180), (300, 300), alpha=True)
            frame.paste(img.rotate(270), (300, 0), alpha=True)
            return frame.rotate(i * 18).crop((50, 50, 550, 550))

        return make

    return make_gif_or_combined_gif(img, maker, 5, 0.05, FrameAlignPolicy.extend_loop)


def littleangel(user: UserInfo = User(), arg: str = Arg()):
    img_w, img_h = user.img.convert("RGBA").resize_width(500).size
    frame = BuildImage.new("RGBA", (600, img_h + 230), "white")
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

    def make(img: BuildImage) -> BuildImage:
        img = img.resize_width(500)
        return frame.copy().paste(img, (int(300 - img_w / 2), 110), alpha=True)

    return make_jpg_or_gif(user.img, make)


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
    img = img.convert("RGBA").square().resize((34, 34))
    frames = []
    for i in range(3):
        frame = load_image(f"eat/{i}.png")
        frame.paste(img, (2, 38), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def klee_eat(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((83, 83))
    # fmt: off
    locs = [
        (0, 174), (0, 174), (0, 174), (0, 174), (0, 174),
        (12, 160), (19, 152), (23, 148), (26, 145), (32, 140),
        (37, 136), (42, 131), (49, 127), (70, 126), (88, 128),
        (-30, 210), (-19, 207), (-14, 200), (-10, 188), (-7, 179),
        (-3, 170), (-3, 175), (-1, 174), (0, 174), (0, 174),
        (0, 174), (0, 174), (0, 174), (0, 174), (0, 174), (0, 174)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(31):
        frame = load_image(f"klee_eat/{i}.png")
        frame.paste(img, locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


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


def hutao_bite(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((100, 100))
    frames: List[IMG] = []
    locs = [(98, 101, 108, 234), (96, 100, 108, 237)]
    for i in range(2):
        frame = load_image(f"hutao_bite/{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


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
    gradient = LinearGradient(
        (0, 0, 0, gradient_h),
        [ColorStop(0, (0, 0, 0, 220)), ColorStop(1, (0, 0, 0, 30))],
    )
    gradient_img = gradient.create_image((img_w, gradient_h))
    mask = BuildImage.new("RGBA", img.size)
    mask.paste(gradient_img, (0, img_h - gradient_h), alpha=True)
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
    img = img.convert("RGBA").resize((515, 383), keep_ratio=True)
    frames: List[IMG] = []
    for i in range(8):
        frames.append(load_image(f"wallpaper/{i}.png").image)
    for i in range(8, 20):
        frame = load_image(f"wallpaper/{i}.png")
        frame.paste(img, (176, -9), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.07)


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
    users: List[UserInfo] = Users(0, 1),
    sender: UserInfo = Sender(),
    name: str = RegexArg("name"),
    args: List[str] = Args(0, 10),
):
    user = users[0] if users else sender
    name = name.strip() or user.name or "朋友"
    texts = args or ["救命啊"]
    img = user.img.convert("RGBA").circle().resize((100, 100))

    name_img = Text2Image.from_text(name, 25, fill="#868894").to_image()
    name_w, name_h = name_img.size
    if name_w >= 600:
        return NAME_TOO_LONG

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
    img = img.convert("RGBA").square().resize((300, 300))
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
    text = arg or "救命啊"
    trans = await translate(text, lang_to="jp")
    img = img.convert("L").resize_width(500)
    text_img1 = BuildImage.new("RGBA", (500, 60))
    text_img2 = BuildImage.new("RGBA", (500, 35))
    try:
        text_img1.draw_text(
            (20, 0, text_img1.width - 20, text_img1.height),
            text,
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

    def make(img: BuildImage) -> BuildImage:
        first = img
        second = img.transpose(mode.method)
        frame = BuildImage.new("RGBA", mode.frame_size)
        frame.paste(first.crop(mode.size1), mode.pos1)
        frame.paste(second.crop(mode.size2), mode.pos2)
        return frame

    return make_jpg_or_gif(img, make, keep_transparency=True)


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
            (5, frame.height - 60, frame.width - 5, frame.height - 10),
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


def keepaway(imgs: List[BuildImage] = UserImgs(1, 8), arg: str = Arg()):
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

    text = arg or "如何提高社交质量 : \n远离以下头像的人"
    frame = BuildImage.new("RGB", (400, 290), "white")
    frame.draw_text((10, 10, 390, 80), text, max_fontsize=40, halign="left")
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


def divorce(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("divorce/0.png")
    img = img.convert("RGBA").resize(frame.size, keep_ratio=True)
    frame.paste(img, below=True)
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


def mywife(user: UserInfo = User(), arg=NoArg()):
    img = user.img.convert("RGBA").resize_width(400)
    img_w, img_h = img.size
    frame = BuildImage.new("RGBA", (650, img_h + 500), "white")
    frame.paste(img, (int(325 - img_w / 2), 105), alpha=True)

    text = "如果你的老婆长这样"
    frame.draw_text(
        (27, 12, 27 + 596, 12 + 79),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        lines_align="center",
        weight="bold",
    )
    text = "那么这就不是你的老婆\n这是我的老婆"
    frame.draw_text(
        (27, img_h + 120, 27 + 593, img_h + 120 + 135),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        weight="bold",
    )
    text = "滚去找你\n自己的老婆去"
    frame.draw_text(
        (27, img_h + 295, 27 + 374, img_h + 295 + 135),
        text,
        max_fontsize=70,
        min_fontsize=30,
        allow_wrap=True,
        lines_align="center",
        weight="bold",
    )

    img_point = load_image("mywife/1.png").resize_width(200)
    frame.paste(img_point, (421, img_h + 270))

    return frame.save_jpg()


def walnutpad(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("walnutpad/0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((540, 360), keep_ratio=True), (368, 65), below=True
        )

    return make_jpg_or_gif(img, make)


def walnut_zoom(img: BuildImage = UserImg(), arg=NoArg()):
    # fmt: off
    locs = (
        (-222, 30, 695, 430), (-212, 30, 695, 430), (0, 30, 695, 430), (41, 26, 695, 430),
        (-100, -67, 922, 570), (-172, -113, 1059, 655), (-273, -192, 1217, 753)
    )
    seq = [0, 0, 0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 4, 5, 6, 6, 6, 6]
    # fmt: on

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            frame = load_image(f"walnut_zoom/{i}.png")
            x, y, w, h = locs[seq[i]]
            img = img.resize((w, h), keep_ratio=True).rotate(4.2, expand=True)
            frame.paste(img, (x, y), below=True)
            return frame

        return make

    return make_gif_or_combined_gif(img, maker, 24, 0.2, FrameAlignPolicy.extend_last)


def teach(img: BuildImage = UserImg(), arg: str = Arg()):
    frame = load_image("teach/0.png").resize_width(960).convert("RGBA")
    try:
        frame.draw_text(
            (10, frame.height - 80, frame.width - 10, frame.height - 5),
            arg,
            max_fontsize=50,
            fill="white",
            stroke_fill="black",
            stroke_ratio=0.06,
        )
    except ValueError:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((550, 395), keep_ratio=True), (313, 60), below=True
        )

    return make_jpg_or_gif(img, make)


def addition(img: BuildImage = UserImg(), arg: str = Arg()):
    frame = load_image("addiction/0.png")

    if arg:
        expand_frame = BuildImage.new("RGBA", (246, 286), "white")
        expand_frame.paste(frame)
        try:
            expand_frame.draw_text(
                (10, 246, 236, 286),
                arg,
                max_fontsize=45,
                lines_align="center",
            )
        except ValueError:
            return TEXT_TOO_LONG
        frame = expand_frame

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(img.resize((91, 91), keep_ratio=True), (0, 0))

    return make_jpg_or_gif(img, make)


def gun(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("gun/0.png")
    frame.paste(img.convert("RGBA").resize((500, 500), keep_ratio=True), below=True)
    return frame.save_jpg()


def blood_pressure(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("blood_pressure/0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((414, 450), keep_ratio=True), (16, 17), below=True
        )

    return make_jpg_or_gif(img, make)


def read_book(img: BuildImage = UserImg(), arg: str = Arg()):
    frame = load_image("read_book/0.png")
    points = ((0, 108), (1092, 0), (1023, 1134), (29, 1134))
    img = img.convert("RGBA").resize((1000, 1100), keep_ratio=True, direction="north")
    cover = img.perspective(points)
    frame.paste(cover, (1138, 1172), below=True)
    if arg:
        chars = list(" ".join(arg.splitlines()))
        pieces: List[BuildImage] = []
        for char in chars:
            piece = BuildImage(
                Text2Image.from_text(char, 200, fill="white", weight="bold").to_image()
            )
            if re.fullmatch(r"[a-zA-Z0-9\s]", char):
                piece = piece.rotate(-90, expand=True)
            else:
                piece = piece.resize_canvas((piece.width, piece.height - 40), "south")
            pieces.append(piece)
        w = max((piece.width for piece in pieces))
        h = sum((piece.height for piece in pieces))
        if w > 265 or h > 3000:
            return TEXT_TOO_LONG
        text_img = BuildImage.new("RGBA", (w, h))
        h = 0
        for piece in pieces:
            text_img.paste(piece, ((w - piece.width) // 2, h), alpha=True)
            h += piece.height
        if h > 780:
            ratio = 780 / h
            text_img = text_img.resize((int(w * ratio), int(h * ratio)))
        text_img = text_img.rotate(3, expand=True)
        w, h = text_img.size
        frame.paste(text_img, (870 + (240 - w) // 2, 1500 + (780 - h) // 2), alpha=True)
    return frame.save_jpg()


def call_110(
    user_imgs: List[BuildImage] = UserImgs(1, 2),
    sender_img: BuildImage = SenderImg(),
    arg=NoArg(),
):
    if len(user_imgs) >= 2:
        img1 = user_imgs[0]
        img0 = user_imgs[1]
    else:
        img1 = sender_img
        img0 = user_imgs[0]
    img1 = img1.convert("RGBA").square().resize((250, 250))
    img0 = img0.convert("RGBA").square().resize((250, 250))

    frame = BuildImage.new("RGB", (900, 500), "white")
    frame.draw_text((0, 0, 900, 200), "遇到困难请拨打", max_fontsize=100)
    frame.paste(img1, (50, 200), alpha=True)
    frame.paste(img1, (325, 200), alpha=True)
    frame.paste(img0, (600, 200), alpha=True)
    return frame.save_jpg()


def confuse(img: BuildImage = UserImg(), arg=NoArg()):
    img_w = min(img.width, 500)

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.resize_width(img_w)
            frame = load_image(f"confuse/{i}.png").resize(img.size, keep_ratio=True)
            bg = BuildImage.new("RGB", img.size, "white")
            bg.paste(img, alpha=True).paste(frame, alpha=True)
            return bg

        return make

    return make_gif_or_combined_gif(
        img, maker, 100, 0.02, FrameAlignPolicy.extend_loop, input_based=True
    )


def hit_screen(img: BuildImage = UserImg(), arg=NoArg()):
    params = (
        (((1, 10), (138, 1), (140, 119), (7, 154)), (32, 37)),
        (((1, 10), (138, 1), (140, 121), (7, 154)), (32, 37)),
        (((1, 10), (138, 1), (139, 125), (10, 159)), (32, 37)),
        (((1, 12), (136, 1), (137, 125), (8, 159)), (34, 37)),
        (((1, 9), (137, 1), (139, 122), (9, 154)), (35, 41)),
        (((1, 8), (144, 1), (144, 123), (12, 155)), (30, 45)),
        (((1, 8), (140, 1), (141, 121), (10, 155)), (29, 49)),
        (((1, 9), (140, 1), (139, 118), (10, 153)), (27, 53)),
        (((1, 7), (144, 1), (145, 117), (13, 153)), (19, 57)),
        (((1, 7), (144, 1), (143, 116), (13, 153)), (19, 57)),
        (((1, 8), (139, 1), (141, 119), (12, 154)), (19, 55)),
        (((1, 13), (140, 1), (143, 117), (12, 156)), (16, 57)),
        (((1, 10), (138, 1), (142, 117), (11, 149)), (14, 61)),
        (((1, 10), (141, 1), (148, 125), (13, 153)), (11, 57)),
        (((1, 12), (141, 1), (147, 130), (16, 150)), (11, 60)),
        (((1, 15), (165, 1), (175, 135), (1, 171)), (-6, 46)),
    )

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.resize((140, 120), keep_ratio=True)
            frame = load_image(f"hit_screen/{i}.png")
            if 6 <= i < 22:
                points, pos = params[i - 6]
                frame.paste(img.perspective(points), pos, below=True)
            return frame

        return make

    return make_gif_or_combined_gif(img, maker, 29, 0.2, FrameAlignPolicy.extend_first)


def fencing(
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
    self_head = self_img.convert("RGBA").circle().resize((27, 27))
    user_head = user_img.convert("RGBA").circle().resize((27, 27))
    # fmt: off
    user_locs = [
        (57, 4), (55, 5), (58, 7), (57, 5), (53, 8), (54, 9),
        (64, 5), (66, 8), (70, 9), (73, 8), (81, 10), (77, 10),
        (72, 4), (79, 8), (50, 8), (60, 7), (67, 6), (60, 6), (50, 9)
    ]
    self_locs = [
        (10, 6), (3, 6), (32, 7), (22, 7), (13, 4), (21, 6),
        (30, 6), (22, 2), (22, 3), (26, 8), (23, 8), (27, 10),
        (30, 9), (17, 6), (12, 8), (11, 7), (8, 6), (-2, 10), (4, 9)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(19):
        frame = load_image(f"fencing/{i}.png")
        frame.paste(user_head, user_locs[i], alpha=True)
        frame.paste(self_head, self_locs[i], alpha=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def hug_leg(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square()
    locs = [
        (50, 73, 68, 92),
        (58, 60, 62, 95),
        (65, 10, 67, 118),
        (61, 20, 77, 97),
        (55, 44, 65, 106),
        (66, 85, 60, 98),
    ]
    frames: List[IMG] = []
    for i in range(6):
        frame = load_image(f"hug_leg/{i}.png")
        x, y, w, h = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.06)


def tankuku_holdsign(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((300, 230), keep_ratio=True)
    params = (
        (((0, 46), (320, 0), (350, 214), (38, 260)), (68, 91)),
        (((18, 0), (328, 28), (298, 227), (0, 197)), (184, 77)),
        (((15, 0), (294, 28), (278, 216), (0, 188)), (194, 65)),
        (((14, 0), (279, 27), (262, 205), (0, 178)), (203, 55)),
        (((14, 0), (270, 25), (252, 195), (0, 170)), (209, 49)),
        (((15, 0), (260, 25), (242, 186), (0, 164)), (215, 41)),
        (((10, 0), (245, 21), (230, 180), (0, 157)), (223, 35)),
        (((13, 0), (230, 21), (218, 168), (0, 147)), (231, 25)),
        (((13, 0), (220, 23), (210, 167), (0, 140)), (238, 21)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((27, 0), (226, 46), (196, 182), (0, 135)), (254, 13)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (175, 9)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (195, 17)),
        (((0, 35), (200, 0), (224, 133), (25, 169)), (195, 17)),
    )
    frames: List[IMG] = []
    for i in range(15):
        points, pos = params[i]
        frame = load_image(f"tankuku_holdsign/{i}.png")
        frame.paste(img.perspective(points), pos, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.2)


def no_response(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((1050, 783), keep_ratio=True)
    frame = load_image("no_response/0.png")
    frame.paste(img, (0, 581), below=True)
    return frame.save_jpg()


def hold_tight(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((159, 171), keep_ratio=True)
    frame = load_image("hold_tight/0.png")
    frame.paste(img, (113, 205), below=True)
    return frame.save_jpg()


def look_flat(img: BuildImage = UserImg(), args: List[str] = Args(0, 2)):
    ratio = 2
    text = "可恶...被人看扁了"
    for arg in args:
        if arg.isdigit():
            ratio = int(arg)
            if ratio < 2 or ratio > 10:
                ratio = 2
        elif arg:
            text = arg

    img_w = 500
    text_h = 80
    text_frame = BuildImage.new("RGBA", (img_w, text_h), "white")
    try:
        text_frame.draw_text(
            (10, 0, img_w - 10, text_h),
            text,
            max_fontsize=55,
            min_fontsize=30,
            weight="bold",
        )
    except ValueError:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize_width(img_w)
        img = img.resize((img_w, img.height // ratio))
        img_h = img.height
        frame = BuildImage.new("RGBA", (img_w, img_h + text_h), "white")
        return frame.paste(img, alpha=True).paste(text_frame, (0, img_h), alpha=True)

    return make_jpg_or_gif(img, make)


def look_this_icon(img: BuildImage = UserImg(), arg: str = Arg()):
    text = arg or "朋友\n先看看这个图标再说话"
    frame = load_image("look_this_icon/nmsl.png")
    try:
        frame.draw_text(
            (0, 933, 1170, 1143),
            text,
            lines_align="center",
            weight="bold",
            max_fontsize=100,
            min_fontsize=50,
        )
    except ValueError:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        img = img.convert("RGBA").resize((515, 515), keep_ratio=True)
        return frame.copy().paste(img, (599, 403), below=True)

    return make_jpg_or_gif(img, make)


def captain(
    user_imgs: List[BuildImage] = UserImgs(1, 5),
    sender_img: BuildImage = SenderImg(),
    arg=NoArg(),
):
    imgs: List[BuildImage] = []
    if len(user_imgs) == 1:
        imgs.append(sender_img)
        imgs.append(user_imgs[0])
        imgs.append(user_imgs[0])
    elif len(user_imgs) == 2:
        imgs.append(user_imgs[0])
        imgs.append(user_imgs[1])
        imgs.append(user_imgs[1])
    else:
        imgs = user_imgs

    bg0 = load_image("captain/0.png")
    bg1 = load_image("captain/1.png")
    bg2 = load_image("captain/2.png")

    frame = BuildImage.new("RGBA", (640, 440 * len(imgs)), "white")
    for i in range(len(imgs)):
        bg = bg0 if i < len(imgs) - 2 else bg1 if i == len(imgs) - 2 else bg2
        imgs[i] = imgs[i].convert("RGBA").square().resize((250, 250))
        bg = bg.copy().paste(imgs[i], (350, 85))
        frame.paste(bg, (0, 440 * i))

    return frame.save_jpg()


def jiji_king(
    user_imgs: List[BuildImage] = UserImgs(1, 11),
    args: List[str] = Args(0, 11),
):
    block_num = 5
    if len(user_imgs) >= 7 or len(args) >= 7:
        block_num = max(len(user_imgs), len(args)) - 1

    chars = ["急"]
    text = "我是急急国王"
    if len(args) == 1:
        if len(user_imgs) == 1:
            chars = [args[0]] * block_num
            text = f"我是{args[0]*2}国王"
        else:
            text = args[0]
    elif len(args) == 2:
        chars = [args[0]] * block_num
        text = args[1]
    elif args:
        chars = sum(
            [[arg] * math.ceil(block_num / len(args[:-1])) for arg in args[:-1]], []
        )
        text = args[-1]

    frame = BuildImage.new("RGBA", (10 + 100 * block_num, 400), "white")
    king = load_image("jiji_king/0.png")
    king.paste(
        user_imgs[0].convert("RGBA").square().resize((125, 125)), (237, 5), alpha=True
    )
    frame.paste(king, ((frame.width - king.width) // 2, 0))

    if len(user_imgs) > 1:
        imgs = user_imgs[1:]
        imgs = [img.convert("RGBA").square().resize((90, 90)) for img in imgs]
    else:
        imgs = []
        for char in chars:
            block = BuildImage.new("RGBA", (90, 90), "black")
            try:
                block.draw_text(
                    (0, 0, 90, 90),
                    char,
                    lines_align="center",
                    weight="bold",
                    max_fontsize=60,
                    min_fontsize=30,
                    fill="white",
                )
            except ValueError:
                return TEXT_TOO_LONG
            imgs.append(block)

    imgs = sum([[img] * math.ceil(block_num / len(imgs)) for img in imgs], [])
    for i in range(block_num):
        frame.paste(imgs[i], (10 + 100 * i, 200))

    try:
        frame.draw_text(
            (10, 300, frame.width - 10, 390),
            text,
            lines_align="center",
            weight="bold",
            max_fontsize=100,
            min_fontsize=30,
        )
    except ValueError:
        return TEXT_TOO_LONG

    return frame.save_jpg()


def incivilization(img: BuildImage = UserImg(), arg: str = Arg()):
    frame = load_image("incivilization/0.png")
    points = ((0, 20), (154, 0), (164, 153), (22, 180))
    img = img.convert("RGBA").circle().resize((150, 150)).perspective(points)
    image = ImageEnhance.Brightness(img.image).enhance(0.8)
    frame.paste(image, (137, 151), alpha=True)
    text = arg or "你刚才说的话不是很礼貌！"
    try:
        frame.draw_text(
            (57, 42, 528, 117),
            text,
            weight="bold",
            max_fontsize=50,
            min_fontsize=20,
            allow_wrap=True,
        )
    except ValueError:
        return TEXT_TOO_LONG
    return frame.save_jpg()


def together(user: UserInfo = User(), arg: str = Arg()):
    frame = load_image("together/0.png")
    frame.paste(user.img.convert("RGBA").resize((63, 63)), (132, 36))
    text = arg or f"一起玩{user.name}吧！"
    try:
        frame.draw_text(
            (10, 140, 190, 190),
            text,
            weight="bold",
            max_fontsize=50,
            min_fontsize=10,
            allow_wrap=True,
        )
    except ValueError:
        return TEXT_TOO_LONG
    return frame.save_jpg()


def wave(img: BuildImage = UserImg(), arg=NoArg()):
    img_w = min(max(img.width, 360), 720)
    period = img_w / 6
    amp = img_w / 60
    frame_num = 8
    phase = 0
    sin = lambda x: amp * math.sin(2 * math.pi / period * (x + phase)) / 2

    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.resize_width(img_w)
            img_h = img.height
            frame = img.copy()
            for i in range(img_w):
                for j in range(img_h):
                    dx = int(sin(i) * (img_h - j) / img_h)
                    dy = int(sin(j) * j / img_h)
                    if 0 <= i + dx < img_w and 0 <= j + dy < img_h:
                        frame.image.putpixel(
                            (i, j), img.image.getpixel((i + dx, j + dy))
                        )

            frame = frame.resize_canvas((int(img_w - amp), int(img_h - amp)))
            nonlocal phase
            phase += period / frame_num
            return frame

        return make

    return make_gif_or_combined_gif(
        img, maker, frame_num, 0.01, FrameAlignPolicy.extend_loop
    )


def rise_dead(img: BuildImage = UserImg(), arg=NoArg()):
    locs = [
        ((81, 55), ((0, 2), (101, 0), (103, 105), (1, 105))),
        ((74, 49), ((0, 3), (104, 0), (106, 108), (1, 108))),
        ((-66, 36), ((0, 0), (182, 5), (184, 194), (1, 185))),
        ((-231, 55), ((0, 0), (259, 4), (276, 281), (13, 278))),
    ]
    img = img.convert("RGBA").square().resize((150, 150))
    imgs = [img.perspective(points) for _, points in locs]
    frames: List[IMG] = []
    for i in range(34):
        frame = load_image(f"rise_dead/{i}.png")
        if i <= 28:
            idx = 0 if i <= 25 else i - 25
            x, y = locs[idx][0]
            if i % 2 == 1:
                x += 1
                y -= 1
            frame.paste(imgs[idx], (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.15)


def kirby_hammer(img: BuildImage = UserImg(), arg: str = Arg(["圆"])):
    # fmt: off
    positions = [
        (318, 163), (319, 173), (320, 183), (317, 193), (312, 199), 
        (297, 212), (289, 218), (280, 224), (278, 223), (278, 220), 
        (280, 215), (280, 213), (280, 210), (280, 206), (280, 201), 
        (280, 192), (280, 188), (280, 184), (280, 179)
    ]
    # fmt: on
    def maker(i: int) -> Maker:
        def make(img: BuildImage) -> BuildImage:
            img = img.convert("RGBA")
            if arg == "圆":
                img = img.circle()
            img = img.resize_height(80)
            if img.width < 80:
                img = img.resize((80, 80), keep_ratio=True)
            frame = load_image(f"kirby_hammer/{i}.png")
            if i <= 18:
                x, y = positions[i]
                x = x + 40 - img.width // 2
                frame.paste(img, (x, y), alpha=True)
            elif i <= 39:
                x, y = positions[18]
                x = x + 40 - img.width // 2
                frame.paste(img, (x, y), alpha=True)
            return frame

        return make

    return make_gif_or_combined_gif(img, maker, 62, 0.05, FrameAlignPolicy.extend_loop)


def wooden_fish(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((85, 85))
    frames = [
        load_image(f"wooden_fish/{i}.png").paste(img, (116, 153), below=True).image
        for i in range(66)
    ]
    return save_gif(frames, 0.1)


def karyl_point(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").rotate(7.5, expand=True).resize((225, 225))
    frame = load_image("karyl_point/0.png")
    frame.paste(img, (87, 790), alpha=True)
    return frame.save_png()


def kick_ball(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((78, 78))
    # fmt: off
    locs = [
        (57, 136), (56, 117), (55, 99), (52, 113), (50, 126),
        (48, 139), (47, 112), (47, 85), (47, 57), (48, 97),
        (50, 136), (51, 176), (52, 169), (55, 181), (58, 153)
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(15):
        frame = load_image(f"kick_ball/{i}.png")
        frame.paste(img.rotate(-24 * i), locs[i], below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def smash(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("smash/0.png")

    def make(img: BuildImage) -> BuildImage:
        points = ((1, 237), (826, 1), (832, 508), (160, 732))
        screen = img.resize((800, 500), keep_ratio=True).perspective(points)
        return frame.copy().paste(screen, (-136, -81), below=True)

    return make_jpg_or_gif(img, make)


def bocchi_draft(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize((350, 400), keep_ratio=True)
    params = [
        (((54, 62), (353, 1), (379, 382), (1, 399)), (146, 173)),
        (((54, 61), (349, 1), (379, 381), (1, 398)), (146, 174)),
        (((54, 61), (349, 1), (379, 381), (1, 398)), (152, 174)),
        (((54, 61), (335, 1), (379, 381), (1, 398)), (158, 167)),
        (((54, 61), (335, 1), (370, 381), (1, 398)), (157, 149)),
        (((41, 59), (321, 1), (357, 379), (1, 396)), (167, 108)),
        (((41, 57), (315, 1), (357, 377), (1, 394)), (173, 69)),
        (((41, 56), (309, 1), (353, 380), (1, 393)), (175, 43)),
        (((41, 56), (314, 1), (353, 380), (1, 393)), (174, 30)),
        (((41, 50), (312, 1), (348, 367), (1, 387)), (171, 18)),
        (((35, 50), (306, 1), (342, 367), (1, 386)), (178, 14)),
    ]
    # fmt: off
    idx = [
        0, 0, 0, 0, 0, 0, 0, 1, 1, 2, 2, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10, 10, 10,
    ]
    # fmt: on
    frames: List[IMG] = []
    for i in range(23):
        frame = load_image(f"bocchi_draft/{i}.png")
        points, pos = params[idx[i]]
        frame.paste(img.perspective(points), pos, below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.08)


def sit_still(user: UserInfo = User(), arg: str = Arg()):
    name = arg or user.name
    frame = load_image("sit_still/0.png")
    try:
        frame.draw_text(
            (100, 170, 600, 330),
            name,
            valign="bottom",
            max_fontsize=75,
            min_fontsize=30,
        )
    except ValueError:
        return NAME_TOO_LONG
    img = user.img.convert("RGBA").circle().resize((150, 150)).rotate(-10, expand=True)
    frame.paste(img, (268, 344), alpha=True)
    return frame.save_jpg()


def learn(img: BuildImage = UserImg(), arg: str = Arg()):
    text = arg or "偷学群友数理基础"
    frame = load_image("learn/0.png")
    try:
        frame.draw_text(
            (100, 1360, frame.width - 100, 1730),
            text,
            max_fontsize=350,
            min_fontsize=200,
            weight="bold",
        )
    except ValueError:
        return TEXT_TOO_LONG

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((1751, 1347), keep_ratio=True), (1440, 0), alpha=True
        )

    return make_jpg_or_gif(img, make)


def trance(img: BuildImage = UserImg(), arg: str = Arg()):
    width, height = img.size
    height1 = int(1.1 * height)
    frame = BuildImage.new("RGB", (width, height1), "white")
    frame.paste(img, (0, int(height * 0.1)))
    img.image.putalpha(3)
    for i in range(int(height * 0.1), 0, -1):
        frame.paste(img, (0, i), alpha=True)
    for i in range(int(height * 0.1), int(height * 0.1 * 2)):
        frame.paste(img, (0, i), alpha=True)
    frame = frame.crop((0, int(0.1 * height), width, height1))
    return frame.save_jpg()


def dinosaur(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("dinosaur/0.png")

    def make(img: BuildImage) -> BuildImage:
        return frame.copy().paste(
            img.resize((680, 578), keep_ratio=True), (294, 369), below=True
        )

    return make_jpg_or_gif(img, make)


def scratch_head(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((68, 68))
    frames: List[IMG] = []
    locs = [
        (53, 46, 4, 5),
        (50, 45, 7, 6),
        (50, 42, 6, 8),
        (50, 44, 7, 7),
        (53, 42, 4, 8),
        (52, 45, 7, 7),
    ]
    for i in range(6):
        frame = load_image(f"scratch_head/{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def applaud(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((110, 110))
    frames: List[IMG] = []
    locs = [
        (109, 102, 27, 17),
        (107, 105, 28, 15),
        (110, 106, 27, 14),
        (109, 106, 27, 14),
        (107, 108, 29, 12),
    ]
    for i in range(5):
        frame = load_image(f"applaud/{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.1)


def chase_train(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").square().resize((42, 42))
    frames: List[IMG] = []
    # fmt: off
    locs = [
        (35, 34, 128, 44), (35, 33, 132, 40), (33, 34, 133, 36), (33, 38, 135, 41),
        (34, 34, 136, 38), (35, 35, 136, 33), (33, 34, 138, 38), (36, 35, 138, 34),
        (38, 34, 139, 32), (40, 35, 139, 37), (36, 35, 139, 33), (39, 36, 138, 28),
        (40, 35, 138, 33), (37, 34, 138, 31), (43, 36, 135, 27), (36, 37, 136, 32),
        (38, 40, 135, 26), (37, 35, 133, 26), (33, 36, 132, 30), (33, 39, 132, 25),
        (32, 36, 131, 23), (33, 36, 130, 31), (35, 39, 128, 25), (33, 35, 127, 23),
        (34, 36, 126, 29), (34, 40, 124, 25), (39, 36, 119, 23), (35, 36, 119, 32),
        (35, 37, 116, 27), (36, 38, 113, 23), (34, 35, 113, 32), (39, 36, 113, 23),
        (36, 35, 114, 17), (36, 38, 111, 13), (34, 37, 114, 15), (34, 39, 111, 10),
        (33, 39, 109, 11), (36, 35, 104, 17), (34, 36, 102, 14), (34, 35, 99, 14),
        (35, 38, 96, 16), (35, 35, 93, 14), (36, 35, 89, 15), (36, 36, 86, 18),
        (36, 39, 83, 14), (34, 36, 81, 16), (40, 41, 74, 17), (38, 36, 74, 15),
        (39, 35, 70, 16), (33, 35, 69, 20), (36, 35, 66, 17), (36, 35, 62, 17),
        (37, 36, 57, 21), (35, 39, 57, 15), (35, 36, 53, 17), (35, 38, 51, 20),
        (37, 36, 47, 19), (37, 35, 47, 18), (40, 36, 43, 19), (38, 35, 42, 22),
        (40, 34, 38, 20), (38, 34, 37, 21), (39, 32, 35, 24), (39, 33, 33, 22),
        (39, 36, 32, 22), (38, 35, 32, 25), (35, 37, 31, 22), (37, 37, 31, 23),
        (36, 31, 31, 28), (37, 34, 32, 25), (36, 37, 32, 23), (36, 33, 33, 30),
        (35, 34, 33, 27), (38, 33, 33, 28), (37, 34, 33, 29), (36, 35, 35, 28),
        (36, 37, 36, 27), (43, 39, 33, 30), (35, 34, 38, 31), (37, 34, 39, 30),
        (36, 34, 40, 30), (39, 35, 41, 30), (41, 36, 41, 29), (40, 37, 44, 32),
        (40, 37, 45, 29), (39, 38, 48, 28), (38, 33, 50, 33), (35, 38, 53, 28),
        (37, 34, 54, 31), (38, 34, 57, 32), (41, 35, 57, 29), (35, 34, 63, 29),
        (41, 35, 62, 29), (38, 35, 66, 28), (35, 33, 70, 29), (40, 39, 70, 28),
        (36, 36, 74, 28), (37, 35, 77, 26), (37, 35, 79, 28), (38, 35, 81, 27),
        (36, 35, 85, 27), (37, 36, 88, 29), (36, 34, 91, 27), (38, 39, 94, 24),
        (39, 34, 95, 27), (37, 34, 98, 26), (36, 35, 103, 24), (37, 36, 99, 28),
        (34, 36, 97, 34), (34, 38, 102, 38), (37, 37, 99, 40), (39, 36, 101, 47),
        (36, 36, 106, 43), (35, 35, 109, 40), (35, 39, 112, 43), (33, 36, 116, 41),
        (36, 36, 116, 39), (34, 37, 121, 45), (35, 41, 123, 38), (34, 37, 126, 35),
    ]
    # fmt: on
    for i in range(120):
        frame = load_image(f"chase_train/{i}.png")
        w, h, x, y = locs[i]
        frame.paste(img.resize((w, h)), (x, y), below=True)
        frames.append(frame.image)
    return save_gif(frames, 0.05)


def kaleidoscope(img: BuildImage = UserImg(), arg: str = Arg(["圆"])):
    def make(img: BuildImage) -> BuildImage:
        circle_num = 10
        img_per_circle = 4
        init_angle = 0
        angle_step = 360 / img_per_circle
        radius = lambda n: n * 50 + 100
        cx = cy = radius(circle_num)

        img = img.convert("RGBA")
        frame = BuildImage.new("RGBA", (cx * 2, cy * 2), "white")
        for i in range(circle_num):
            r = radius(i)
            img_w = i * 35 + 100
            im = img.resize_width(img_w)
            if arg == "圆":
                im = im.circle()
            for j in range(img_per_circle):
                angle = init_angle + angle_step * j
                im_rot = im.rotate(angle - 90, expand=True)
                x = round(cx + r * math.cos(math.radians(angle)) - im_rot.width / 2)
                y = round(cy - r * math.sin(math.radians(angle)) - im_rot.height / 2)
                frame.paste(im_rot, (x, y), alpha=True)
            init_angle += angle_step / 2
        return frame

    return make_jpg_or_gif(img, make)


def overtime(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("overtime/0.png")
    img = img.convert("RGBA").resize((250, 250), keep_ratio=True)
    frame.paste(img.rotate(-25, expand=True), (165, 220), below=True)
    return frame.save_jpg()


def avatar_formula(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("avatar_formula/0.png")
    img_c = img.convert("RGBA").circle().resize((72, 72))
    img_tp = img.convert("RGBA").circle().resize((51, 51))
    frame.paste(img_tp, (948, 247))
    # fmt: off
    locs = [
        (143, 32), (155, 148), (334, 149), (275, 266), (486, 266),
        (258, 383), (439, 382), (343, 539), (577, 487), (296, 717),
        (535, 717), (64, 896), (340, 896), (578, 897), (210, 1038),
        (644, 1039), (64, 1192), (460, 1192), (698, 1192), (1036, 141),
        (1217, 141), (1243, 263), (1140, 378), (1321, 378), (929, 531),
        (1325, 531), (1592, 531), (1007, 687), (1390, 687), (1631, 686),
        (1036, 840), (1209, 839), (1447, 839), (1141, 1018), (1309, 1019),
        (1546, 1019), (1037, 1197), (1317, 1198), (1555, 1197),
    ]
    # fmt: on
    for i in range(39):
        x, y = locs[i]
        frame.paste(img_c, (x, y))
    return frame.save_jpg()


def potato(img: BuildImage = UserImg(), arg=NoArg()):
    frame = load_image("potato/0.png")
    img = img.convert("RGBA").square().resize((458, 458))
    frame.paste(img.rotate(-5), (531, 15), below=True)
    return frame.save_jpg()


def printing(img: BuildImage = UserImg(), arg=NoArg()):
    img = img.convert("RGBA").resize(
        (304, 174), keep_ratio=True, inside=True, bg_color="white", direction="south"
    )
    frames = [load_image(f"printing/{i}.png") for i in range(115)]
    for i in range(50, 115):
        frames[i].paste(img, (146, 164), below=True)
    frames = [frame.image for frame in frames]
    return save_gif(frames, 0.05)
