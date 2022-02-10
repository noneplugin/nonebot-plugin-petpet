import random
from io import BytesIO
from typing import Union, List
from PIL.Image import Image as IMG
from PIL import Image, ImageFilter, ImageDraw

from .models import UserInfo
from .utils import (
    DEFAULT_FONT,
    circle,
    rotate,
    resize,
    perspective,
    to_jpg,
    save_jpg,
    save_gif,
    load_image,
    load_font,
    fit_font_size,
)


async def petpet(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frames = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    for i in range(5):
        frame = Image.new("RGBA", (112, 112), (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        hand = await load_image(f"petpet/{i}.png")
        frame.paste(hand, mask=hand)
        frames.append(frame)
    return save_gif(frames, 0.06)


async def kiss(users: List[UserInfo], sender: UserInfo, **kwargs) -> BytesIO:
    if len(users) >= 2:
        self_img = users[0].img
        user_img = users[1].img
    else:
        self_img = sender.img
        user_img = users[0].img
    user_locs = [
        (58, 90),
        (62, 95),
        (42, 100),
        (50, 100),
        (56, 100),
        (18, 120),
        (28, 110),
        (54, 100),
        (46, 100),
        (60, 100),
        (35, 115),
        (20, 120),
        (40, 96),
    ]
    self_locs = [
        (92, 64),
        (135, 40),
        (84, 105),
        (80, 110),
        (155, 82),
        (60, 96),
        (50, 80),
        (98, 55),
        (35, 65),
        (38, 100),
        (70, 80),
        (84, 65),
        (75, 65),
    ]
    frames = []
    for i in range(13):
        frame = await load_image(f"kiss/{i}.png")
        user_head = resize(circle(user_img), (50, 50))
        frame.paste(user_head, user_locs[i], mask=user_head)
        self_head = resize(circle(self_img), (40, 40))
        frame.paste(self_head, self_locs[i], mask=self_head)
        frames.append(frame)
    return save_gif(frames, 0.05)


async def rub(users: List[UserInfo], sender: UserInfo, **kwargs) -> BytesIO:
    if len(users) >= 2:
        self_img = users[0].img
        user_img = users[1].img
    else:
        self_img = sender.img
        user_img = users[0].img
    user_locs = [
        (39, 91, 75, 75),
        (49, 101, 75, 75),
        (67, 98, 75, 75),
        (55, 86, 75, 75),
        (61, 109, 75, 75),
        (65, 101, 75, 75),
    ]
    self_locs = [
        (102, 95, 70, 80, 0),
        (108, 60, 50, 100, 0),
        (97, 18, 65, 95, 0),
        (65, 5, 75, 75, -20),
        (95, 57, 100, 55, -70),
        (109, 107, 65, 75, 0),
    ]
    frames = []
    for i in range(6):
        frame = await load_image(f"rub/{i}.png")
        x, y, w, h = user_locs[i]
        user_head = resize(circle(user_img), (w, h))
        frame.paste(user_head, (x, y), mask=user_head)
        x, y, w, h, angle = self_locs[i]
        self_head = rotate(resize(circle(self_img), (w, h)), angle)
        frame.paste(self_head, (x, y), mask=self_head)
        frames.append(frame)
    return save_gif(frames, 0.05)


async def play(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    locs = [
        (180, 60, 100, 100),
        (184, 75, 100, 100),
        (183, 98, 100, 100),
        (179, 118, 110, 100),
        (156, 194, 150, 48),
        (178, 136, 122, 69),
        (175, 66, 122, 85),
        (170, 42, 130, 96),
        (175, 34, 118, 95),
        (179, 35, 110, 93),
        (180, 54, 102, 93),
        (183, 58, 97, 92),
        (174, 35, 120, 94),
        (179, 35, 109, 93),
        (181, 54, 101, 92),
        (182, 59, 98, 92),
        (183, 71, 90, 96),
        (180, 131, 92, 101),
    ]
    raw_frames = []
    for i in range(23):
        raw_frame = await load_image(f"play/{i}.png")
        raw_frames.append(raw_frame)
    img_frames = []
    for i in range(len(locs)):
        frame = Image.new("RGBA", (480, 400), (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        raw_frame = raw_frames[i]
        frame.paste(raw_frame, mask=raw_frame)
        img_frames.append(frame)
    frames = []
    for i in range(2):
        frames.extend(img_frames[0:12])
    frames.extend(img_frames[0:8])
    frames.extend(img_frames[12:18])
    frames.extend(raw_frames[18:23])
    return save_gif(frames, 0.06)


async def pat(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    locs = [(11, 73, 106, 100), (8, 79, 112, 96)]
    img_frames = []
    for i in range(10):
        frame = Image.new("RGBA", (235, 196), (255, 255, 255, 0))
        x, y, w, h = locs[1] if i == 2 else locs[0]
        frame.paste(resize(img, (w, h)), (x, y))
        raw_frame = await load_image(f"pat/{i}.png")
        frame.paste(raw_frame, mask=raw_frame)
        img_frames.append(frame)
    seq = [
        0,
        1,
        2,
        3,
        1,
        2,
        3,
        0,
        1,
        2,
        3,
        0,
        0,
        1,
        2,
        3,
        0,
        0,
        0,
        0,
        4,
        5,
        5,
        5,
        6,
        7,
        8,
        9,
    ]
    frames = [img_frames[n] for n in seq]
    return save_gif(frames, 0.085)


async def rip(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    rip = await load_image("rip/0.png")
    frame = Image.new("RGBA", rip.size, (255, 255, 255, 0))
    left = rotate(resize(img, (385, 385)), 24)
    right = rotate(resize(img, (385, 385)), -11)
    frame.paste(left, (-5, 355))
    frame.paste(right, (649, 310))
    frame.paste(rip, mask=rip)
    return save_jpg(frame)


async def throw(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = resize(rotate(circle(img), random.randint(1, 360), expand=False), (143, 143))
    frame = await load_image("throw/0.png")
    frame.paste(img, (15, 178), mask=img)
    return save_jpg(frame)


async def crawl(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = resize(circle(img), (100, 100))
    frame = await load_image("crawl/{:02d}.jpg".format(random.randint(1, 92)))
    frame.paste(img, (0, 400), mask=img)
    return save_jpg(frame)


async def support(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    support = await load_image("support/0.png")
    frame = Image.new("RGBA", support.size, (255, 255, 255, 0))
    img = rotate(resize(img, (815, 815)), 23)
    frame.paste(img, (-172, -17))
    frame.paste(support, mask=support)
    return save_jpg(frame)


async def always(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    always = await load_image("always/0.png")
    w, h = img.size
    h1 = int(h / w * 300)
    h2 = int(h / w * 60)
    height = h1 + h2 + 10

    def paste(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", (300, height), (255, 255, 255, 0))
        frame.paste(always, (0, h1 - 300 + int((h2 - 60) / 2)))
        frame.paste(resize(img, (300, h1)), (0, 0))
        frame.paste(resize(img, (60, h2)), (165, h1 + 5))
        return frame

    if not getattr(img, "is_animated", False):
        return save_jpg(paste(img))
    else:
        frames = []
        for i in range(img.n_frames):
            img.seek(i)
            frames.append(paste(img))
        return save_gif(frames, img.info["duration"] / 1000)


async def loading(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("loading/0.png")
    icon = await load_image("loading/1.png")
    w, h = img.size
    h1 = int(h / w * 300)
    h2 = int(h / w * 60)
    height = h1 + h2 + 10

    def paste_large(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", (300, height), (255, 255, 255, 0))
        frame.paste(bg, (0, h1 - 300 + int((h2 - 60) / 2)))
        img = resize(img, (300, h1))
        img = img.filter(ImageFilter.GaussianBlur(radius=2))
        frame.paste(img, (0, 0))
        mask = Image.new("RGBA", (300, h1), (0, 0, 0, 128))
        frame.paste(mask, (0, 0), mask=mask)
        frame.paste(icon, (100, int(h1 / 2) - 50), mask=icon)
        return frame

    def paste_small(frame: IMG, img: IMG) -> IMG:
        img = to_jpg(img)
        frame.paste(resize(img, (60, h2)), (60, h1 + 5))
        return frame

    if not getattr(img, "is_animated", False):
        return save_jpg(paste_small(paste_large(img), img))
    else:
        frames = []
        frame = paste_large(img)
        for i in range(img.n_frames):
            img.seek(i)
            frames.append(paste_small(frame.copy(), img))
        return save_gif(frames, img.info["duration"] / 1000)


async def turn(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = circle(img)
    frames = []
    for i in range(0, 360, 10):
        frame = Image.new("RGBA", (250, 250), (255, 255, 255, 0))
        frame.paste(resize(rotate(img, i, False), (250, 250)), (0, 0))
        frames.append(to_jpg(frame))
    if random.randint(0, 1):
        frames.reverse()
    return save_gif(frames, 0.05)


async def littleangel(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    img_w, img_h = img.size
    max_len = max(img_w, img_h)
    img_w = int(img_w * 500 / max_len)
    img_h = int(img_h * 500 / max_len)
    img = resize(img, (img_w, img_h))

    bg = Image.new("RGB", (600, img_h + 230), (255, 255, 255))
    bg.paste(img, (int(300 - img_w / 2), 110))
    draw = ImageDraw.Draw(bg)
    fontname = "SourceHanSansSC-Bold.otf"

    font = await load_font(fontname, 48)
    text = "非常可爱！简直就是小天使"
    text_w, _ = font.getsize(text)
    draw.text((300 - text_w / 2, img_h + 120), text, font=font, fill=(0, 0, 0))

    font = await load_font(fontname, 26)
    ta = "他" if users[0].gender == "male" else "她"
    text = f"{ta}没失踪也没怎么样  我只是觉得你们都该看一下"
    text_w, _ = font.getsize(text)
    draw.text((300 - text_w / 2, img_h + 180), text, font=font, fill=(0, 0, 0))

    name = (args and args[0]) or users[0].name or ta
    text = f"请问你们看到{name}了吗?"
    fontsize = await fit_font_size(text, 560, 110, fontname, 70, 25)
    if not fontsize:
        return "名字太长了哦，改短点再试吧~"

    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize(text)
    x = 300 - text_w / 2
    y = 55 - text_h / 2
    draw.text((x, y), text, font=font, fill=(0, 0, 0))
    return save_jpg(bg)


async def dont_touch(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frame = await load_image("dont_touch/0.png")
    frame.paste(resize(img, (170, 170)), (23, 231))
    return save_jpg(frame)


async def alike(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frame = await load_image("alike/0.png")
    frame.paste(resize(img, (90, 90)), (131, 14))
    return save_jpg(frame)


async def roll(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frames = []
    locs = [
        (87, 77, 0),
        (96, 85, -45),
        (92, 79, -90),
        (92, 78, -135),
        (92, 75, -180),
        (92, 75, -225),
        (93, 76, -270),
        (90, 80, -315),
    ]
    for i in range(8):
        frame = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
        x, y, a = locs[i]
        frame.paste(rotate(resize(img, (210, 210)), a, expand=False), (x, y))
        bg = await load_image(f"roll/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def play_game(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    img_w, img_h = img.size
    sc_w, sc_h = (220, 160)
    ratio = min(sc_w / img_w, sc_h / img_h)
    img_w = int(img_w * ratio)
    img_h = int(img_h * ratio)
    img = resize(img, (img_w, img_h))

    screen = Image.new("RGB", (sc_w, sc_h), (0, 0, 0))
    screen.paste(img, (int((sc_w - img_w) / 2), int((sc_h - img_h) / 2)))
    points = [(0, 5), (225, 0), (215, 150), (0, 165)]
    screen = rotate(perspective(screen, points), 9)

    bg = await load_image("play_game/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(screen, (161, 117))
    frame.paste(bg, mask=bg)

    font = await load_font(DEFAULT_FONT, 35)
    draw = ImageDraw.Draw(frame)
    draw.text(
        (150, 430),
        "来玩休闲游戏啊",
        font=font,
        fill="#000000",
        stroke_fill="#FFFFFF",
        stroke_width=2,
    )
    return save_jpg(frame)


async def worship(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    points = [(0, -30), (135, 17), (135, 145), (0, 140)]
    paint = perspective(img, points)
    frames = []
    for i in range(10):
        frame = Image.new("RGBA", (300, 169), (255, 255, 255, 0))
        frame.paste(paint)
        bg = await load_image(f"worship/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)
