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
    motion_blur,
    square,
    fit_size,
    FitSizeMode,
    FitSizeDir,
    to_jpg,
    save_jpg,
    save_gif,
    make_jpg_or_gif,
    load_image,
    load_font,
    fit_font_size,
)


async def petpet(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    frames = []
    locs = [
        (14, 20, 98, 98),
        (12, 33, 101, 85),
        (8, 40, 110, 76),
        (10, 33, 102, 84),
        (12, 20, 98, 98),
    ]
    if args and "圆" in args[0]:
        img = circle(img)
    for i in range(5):
        frame = Image.new("RGBA", (112, 112), (255, 255, 255, 0))
        x, y, w, h = locs[i]
        new_img = resize(img, (w, h))
        frame.paste(new_img, (x, y), mask=new_img)
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
    # fmt: off
    seq = [0, 1, 2, 3, 1, 2, 3, 0, 1, 2, 3, 0, 0, 1, 2, 3, 0, 0, 0, 0, 4, 5, 5, 5, 6, 7, 8, 9]
    # fmt: on
    frames = [img_frames[n] for n in seq]
    return save_gif(frames, 0.085)


async def rip(
    users: List[UserInfo], sender: UserInfo, args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    if len(users) >= 2:
        self_img = users[0].img
        user_img = users[1].img
    else:
        self_img = sender.img
        user_img = users[0].img

    arg = "".join(args)
    if "滑稽" in arg:
        rip = await load_image("rip/0.png")
    else:
        rip = await load_image("rip/1.png")
    text = arg.strip("滑稽").strip()

    frame = Image.new("RGBA", rip.size, (255, 255, 255, 0))
    left = rotate(resize(user_img, (385, 385)), 24)
    right = rotate(resize(user_img, (385, 385)), -11)
    frame.paste(left, (-5, 355))
    frame.paste(right, (649, 310))
    frame.paste(resize(self_img, (230, 230)), (408, 418))
    frame.paste(rip, mask=rip)

    if text:
        fontname = DEFAULT_FONT
        fontsize = await fit_font_size(text, rip.width - 50, 300, fontname, 150, 25)
        if not fontsize:
            return "文字太长了哦，改短点再试吧~"
        font = await load_font(fontname, fontsize)
        text_w = font.getsize(text)[0]
        draw = ImageDraw.Draw(frame)
        draw.text(
            ((rip.width - text_w) / 2, 40),
            text,
            font=font,
            fill="#FF0000",
            stroke_width=2,
        )
    return save_jpg(frame)


async def throw(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = resize(rotate(circle(img), random.randint(1, 360), expand=False), (143, 143))
    frame = await load_image("throw/0.png")
    frame.paste(img, (15, 178), mask=img)
    return save_jpg(frame)


async def throw_gif(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
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
    frames = []
    for i in range(8):
        frame = await load_image(f"throw_gif/{i}.png")
        for w, h, x, y in locs[i]:
            new_img = resize(circle(img), (w, h))
            frame.paste(new_img, (x, y), mask=new_img)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def crawl(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = resize(circle(img), (100, 100))
    crawl_total = 92
    crawl_num = random.randint(1, crawl_total)
    if args and args[0].isdigit() and 1 <= int(args[0]) <= crawl_total:
        crawl_num = int(args[0])
    frame = await load_image("crawl/{:02d}.jpg".format(crawl_num))
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

    def make(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", (300, height), (255, 255, 255, 0))
        frame.paste(always, (0, h1 - 300 + int((h2 - 60) / 2)))
        frame.paste(resize(img, (300, h1)), (0, 0))
        frame.paste(resize(img, (60, h2)), (165, h1 + 5))
        return frame

    return make_jpg_or_gif(img, make)


async def loading(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("loading/0.png")
    icon = await load_image("loading/1.png")
    w, h = img.size
    h1 = int(h / w * 300)
    h2 = int(h / w * 60)
    height = h1 + h2 + 10

    def make_static(img: IMG) -> IMG:
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

    frame = make_static(img)

    def make(img: IMG) -> IMG:
        new_img = frame.copy()
        new_img.paste(resize(img, (60, h2)), (60, h1 + 5))
        return new_img

    return make_jpg_or_gif(img, make)


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

    name = (args[0] if args else "") or users[0].name or ta
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
    # fmt: off
    locs = [
        (87, 77, 0), (96, 85, -45), (92, 79, -90), (92, 78, -135),
        (92, 75, -180), (92, 75, -225), (93, 76, -270), (90, 80, -315)
    ]
    # fmt: on
    for i in range(8):
        frame = Image.new("RGBA", (300, 300), (255, 255, 255, 0))
        x, y, a = locs[i]
        frame.paste(rotate(resize(img, (210, 210)), a, expand=False), (x, y))
        bg = await load_image(f"roll/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def play_game(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    bg = await load_image("play_game/0.png")
    text = args[0] if args else "来玩休闲游戏啊"
    fontname = DEFAULT_FONT
    fontsize = await fit_font_size(text, 520, 110, fontname, 35, 25)
    if not fontsize:
        return "描述太长了哦，改短点再试吧~"
    font = await load_font(fontname, fontsize)
    text_w = font.getsize(text)[0]

    def make(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        points = [(0, 5), (227, 0), (216, 150), (0, 165)]
        screen = rotate(perspective(fit_size(img, (220, 160)), points), 9)
        frame.paste(screen, (161, 117))
        frame.paste(bg, mask=bg)

        draw = ImageDraw.Draw(frame)
        draw.text(
            (263 - text_w / 2, 430),
            text,
            font=font,
            fill="#000000",
            stroke_fill="#FFFFFF",
            stroke_width=2,
        )
        return frame

    return make_jpg_or_gif(img, make)


async def worship(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    points = [(0, -30), (135, 17), (135, 145), (0, 140)]
    paint = perspective(resize(img, (150, 150)), points)
    frames = []
    for i in range(10):
        frame = Image.new("RGBA", (300, 169), (255, 255, 255, 0))
        frame.paste(paint)
        bg = await load_image(f"worship/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)


async def eat(users: List[UserInfo], **kwargs) -> BytesIO:
    img = resize(users[0].img, (32, 32))
    frames = []
    for i in range(3):
        frame = Image.new("RGBA", (60, 67), (255, 255, 255, 0))
        frame.paste(img, (1, 38))
        bg = await load_image(f"eat/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.05)


async def bite(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    raw_frames = []
    for i in range(16):
        raw_frame = await load_image(f"bite/{i}.png")
        raw_frames.append(raw_frame)
    frames = []
    # fmt: off
    locs = [
        (90, 90, 105, 150), (90, 83, 96, 172), (90, 90, 106, 148),
        (88, 88, 97, 167), (90, 85, 89, 179), (90, 90, 106, 151)
    ]
    # fmt: on
    for i in range(6):
        frame = Image.new("RGBA", (362, 364), (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        raw_frame = await load_image(f"bite/{i}.png")
        frame.paste(raw_frame, mask=raw_frame)
        frames.append(frame)
    frames.extend(raw_frames[6:])
    return save_gif(frames, 0.07)


async def police(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("police/0.png")
    frame = Image.new("RGBA", bg.size)
    frame.paste(resize(img, (245, 245)), (224, 46))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def police1(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    bg = await load_image("police/1.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(rotate(fit_size(img, (60, 75)), 16), (37, 291))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def ask(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    img = resize(img, (640, int(img.height * 640 / img.width)))

    img_w, img_h = img.size
    mask_h = 150
    start_t = 180
    gradient = Image.new("L", (1, img_h))
    for y in range(img_h):
        t = 0 if y < img_h - mask_h else img_h - y + start_t - mask_h
        gradient.putpixel((0, y), t)
    alpha = gradient.resize((img_w, img_h))
    mask = Image.new("RGBA", (img_w, img_h))
    mask.putalpha(alpha)
    mask = mask.filter(ImageFilter.GaussianBlur(radius=3))
    img = Image.alpha_composite(img, mask)

    name = (args[0] if args else "") or users[0].name
    ta = "他" if users[0].gender == "male" else "她"
    if not name:
        return "找不到名字，加上名字再试吧~"

    font = await load_font("SourceHanSansSC-Bold.otf", 25)
    draw = ImageDraw.Draw(img)
    start_h = img_h - mask_h
    start_w = 30
    text_w = font.getsize(name)[0]
    line_w = text_w + 200
    draw.text(
        (start_w + (line_w - text_w) / 2, start_h + 5), name, font=font, fill="orange"
    )
    draw.line(
        (start_w, start_h + 45, start_w + line_w, start_h + 45), fill="orange", width=2
    )
    text_w = font.getsize(f"{name}不知道哦")[0]
    draw.text(
        (start_w + (line_w - text_w) / 2, start_h + 50),
        f"{name}不知道哦。",
        font=font,
        fill="white",
    )

    sep_w = 30
    sep_h = 80
    bg = Image.new("RGBA", (img_w + sep_w * 2, img_h + sep_h * 2), "white")
    font = await load_font("SourceHanSansSC-Regular.otf", 35)
    if font.getsize(name)[0] > 600:
        return "名字太长了哦，改短点再试吧~"
    draw = ImageDraw.Draw(bg)
    draw.text((sep_w, 10), f"让{name}告诉你吧", font=font, fill="black")
    draw.text((sep_w, sep_h + img_h + 10), f"啊这，{ta}说不知道", font=font, fill="black")
    bg.paste(img, (sep_w, sep_h))
    return save_jpg(bg)


async def prpr(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("prpr/0.png")

    def make(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        points = [(0, 19), (236, 0), (287, 264), (66, 351)]
        screen = perspective(fit_size(img, (330, 330)), points)
        frame.paste(screen, (56, 284))
        frame.paste(bg, mask=bg)
        return frame

    return make_jpg_or_gif(img, make)


async def twist(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frames = []
    # fmt: off
    locs = [
        (25, 66, 0), (25, 66, 60), (23, 68, 120),
        (20, 69, 180), (22, 68, 240), (25, 66, 300)
    ]
    # fmt: on
    for i in range(5):
        frame = Image.new("RGBA", (166, 168), (255, 255, 255, 0))
        x, y, a = locs[i]
        frame.paste(rotate(resize(img, (78, 78)), a, expand=False), (x, y))
        bg = await load_image(f"twist/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def wallpaper(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("wallpaper/0.png")

    def make(img: IMG) -> IMG:
        img = to_jpg(img)
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame.paste(fit_size(img, (775, 496)), (260, 580))
        frame.paste(bg, mask=bg)
        return frame

    return make_jpg_or_gif(img, make, gif_zoom=0.5)


async def china_flag(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("china_flag/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(resize(img, bg.size))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def make_friend(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    img = resize(img, (1000, int(img.height * 1000 / img.width)))

    bg = await load_image("make_friend/0.png")
    frame = img.copy()
    frame.paste(
        rotate(resize(img, (250, int(250 / img.width * img.height))), 9),
        (743, img.height - 155),
    )
    frame.paste(rotate(resize(square(img), (55, 55)), 9), (836, img.height - 278))
    frame.paste(bg, (0, img.height - 1000), mask=bg)
    font = await load_font(DEFAULT_FONT, 40)

    name = (args[0] if args else "") or users[0].name
    if not name:
        return "找不到名字，加上名字再试吧~"
    text_frame = Image.new("RGBA", (500, 50))
    draw = ImageDraw.Draw(text_frame)
    draw.text((0, -10), name, font=font, fill="#FFFFFF")
    text_frame = rotate(resize(text_frame, (250, 25)), 9)
    frame.paste(text_frame, (710, img.height - 340), mask=text_frame)
    return save_jpg(frame)


async def back_to_work(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    bg = await load_image("back_to_work/1.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    new_img = fit_size(img, (220, 310), direction=FitSizeDir.NORTH)
    frame.paste(rotate(new_img, 25), (56, 32))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def perfect(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    frame = await load_image("perfect/0.png")
    new_img = fit_size(img, (310, 460), mode=FitSizeMode.INSIDE)
    frame.paste(new_img, (313, 64), mask=new_img)
    return save_jpg(frame)


async def follow(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    img = resize(circle(img), (200, 200))

    font = await load_font(DEFAULT_FONT, 60)
    ta = "女同" if users[0].gender == "female" else "男同"
    name = (args[0] if args else "") or users[0].name or ta
    text_name = name
    text_name_w, text_name_h = font.getsize(text_name)
    text_follow = "关注了你"
    text_width = max(text_name_w, font.getsize(text_follow)[0])
    if text_width >= 1000:
        return "名字太长了哦，改短点再试吧~"

    frame = Image.new("RGBA", (300 + text_width + 50, 300), (255, 255, 255, 0))
    frame.paste(img, (50, 50), mask=img)
    text_frame = Image.new("RGBA", (text_width + 50, 300), (255, 255, 255, 0))
    draw = ImageDraw.Draw(text_frame)
    draw.text((0, 135 - text_name_h), text_name, font=font, fill="black")
    draw.text((0, 145), text_follow, font=font, fill="grey")
    frame.paste(text_frame, (300, 0), mask=text_frame)

    return save_jpg(frame)


async def my_friend(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    if not args:
        return "你朋友说啥？"
    elif len(args) <= 1:
        name = users[0].name or "朋友"
        text = args[0]
    else:
        name = args[0] or "朋友"
        text = args[1]
    text = text.replace("他", "我").replace("她", "我").replace("它", "我")

    name_font = await load_font(DEFAULT_FONT, 25)
    text_font = await load_font(DEFAULT_FONT, 40)
    name_w, name_h = name_font.getsize(name)
    text_w, text_h = text_font.getsize(text)
    if name_w >= 800:
        return "名字太长了哦，改短点再试吧~"
    if text_w >= 1000:
        return "文本太长了哦，改短点再试吧~"

    dialog_left = await load_image("my_friend/0.png")
    dialog_right = await load_image("my_friend/1.png")
    dialog_box = Image.new("RGBA", (max(text_w, name_w + 15) + 140, 150))
    dialog_box.paste(dialog_left, (0, 0))
    dialog_box.paste(Image.new("RGBA", (text_w, 110), "#ffffff"), (70, 20))
    dialog_box.paste(dialog_right, (text_w + 70, 0))
    draw = ImageDraw.Draw(dialog_box)
    draw.text((70, 15 + (110 - text_h) / 2), text, font=text_font, fill="#000000")

    img = resize(circle(img), (100, 100))
    frame = Image.new("RGBA", (dialog_box.width + 130, 210), "#eaedf4")
    frame.paste(img, (20, 20), mask=img)
    frame.paste(dialog_box, (130, 60), mask=dialog_box)
    label = await load_image("my_friend/2.png")
    frame.paste(label, (160, 25))
    draw = ImageDraw.Draw(frame)
    draw.text((260, 22 + (35 - name_h) / 2), name, font=name_font, fill="#868894")
    return save_jpg(frame)


async def paint(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = to_jpg(img).convert("RGBA")
    bg = await load_image("paint/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(rotate(fit_size(img, (117, 135)), 4), (95, 107))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def shock(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = resize(img, (300, 300))
    frames = []
    # fmt: off
    params = [
        (15, 0, 30), (-15, 90, 10), (-15, -45, 25), (-15, 45, 10),
        (15, 45, 20), (0, -60, 30), (-10, 20, 10), (-15, 0, 0),
        (-20, 0, 0), (0, 90, 40), (0, -70, 20), (0, 0, 20),
        (-10, 90, 5), (-20, 90, 40), (-10, 0, 0), (15, 90, 10),
        (10, 0, 10), (10, 0, 5), (-20, 90, 5), (-5, -45, 20),
        (15, 0, 5), (0, 90, 5), (10, 80, 10), (-15, -45, 20),
        (0, 0, 20), (20, 0, 10), (0, 45, 30), (-10, 90, 5),
        (15, 0, 5), (-10, 0, 5)
    ]
    # fmt: on
    for angle, blur_angle, blur_degree in params:
        frames.append(
            rotate(motion_blur(img, blur_angle, blur_degree), angle, expand=False)
        )
    return save_gif(frames, 0.001)


async def coupon(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> Union[str, BytesIO]:
    img = users[0].img
    bg = await load_image("coupon/0.png")
    new_img = rotate(resize(circle(img), (60, 60)), 22)
    bg.paste(new_img, (164, 85), mask=new_img)

    font = await load_font(DEFAULT_FONT, 30)
    text_img = Image.new("RGBA", (250, 100))
    text = f"{users[0].name}陪睡券" if not args else args[0]
    text += "\n（永久有效）"
    text_w = font.getsize_multiline(text)[0]
    if text_w > text_img.width:
        return "文字太长了哦，改短点再试吧~"

    draw = ImageDraw.Draw(text_img)
    draw.multiline_text(
        ((text_img.width - text_w) / 2, 0),
        text,
        font=font,
        align="center",
        fill="#000000",
    )
    text_img = rotate(text_img, 22)
    bg.paste(text_img, (94, 108), mask=text_img)
    return save_jpg(bg)
