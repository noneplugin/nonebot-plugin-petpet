import random
from io import BytesIO
from typing import List
from PIL.Image import Image as IMG
from PIL import Image, ImageFilter, ImageDraw, ImageOps

from .models import UserInfo
from .utils import *


TEXT_TOO_LONG = "文字太长了哦，改短点再试吧~"
NAME_TOO_LONG = "名字太长了哦，改短点再试吧~"
REQUIRE_NAME = "找不到名字，加上名字再试吧~"
REQUIRE_ARG = "该表情至少需要一个参数"


async def operations(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    help_msg = "支持的操作：水平翻转、垂直翻转、黑白、旋转、反相、浮雕、轮廓、锐化"
    if not args:
        raise ValueError(help_msg)

    op = args[0]
    if op == "倒放" and getattr(img, "is_animated", False):
        duration = img.info["duration"] / 1000
        frames = []
        for i in range(img.n_frames):
            img.seek(i)
            frames.append(img.convert("RGB"))
        frames.reverse()
        return save_gif(frames, duration)

    async def make(img: IMG) -> IMG:
        if op == "水平翻转":
            frame = img.transpose(Image.FLIP_LEFT_RIGHT)
        elif op == "垂直翻转":
            frame = img.transpose(Image.FLIP_TOP_BOTTOM)
        elif op == "黑白":
            frame = img.convert("L")
        elif op == "旋转":
            angle = int(args[1]) if args[1:] and args[1].isdigit() else 90
            frame = rotate(img, int(angle))
        elif op == "反相":
            img = img.convert("RGB")
            frame = ImageOps.invert(img)
        elif op == "浮雕":
            frame = img.filter(ImageFilter.EMBOSS)
        elif op == "轮廓":
            frame = img.filter(ImageFilter.CONTOUR)
        elif op == "锐化":
            frame = img.filter(ImageFilter.SHARPEN)
        else:
            raise ValueError(help_msg)
        return frame

    return await make_jpg_or_gif(img, make)


async def universal(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    if not args:
        args = ["万能表情"]

    img_w, img_h = limit_size(img, (500, 500), FitSizeMode.INSIDE).size
    fontname = DEFAULT_FONT
    min_fontsize = 50
    for a in args:
        fontsize = await fit_font_size(a, img_w - 20, img_h, fontname, 50, 10)
        if not fontsize:
            raise ValueError(TEXT_TOO_LONG)
        if fontsize < min_fontsize:
            min_fontsize = fontsize

    async def make(img: IMG) -> IMG:
        img = limit_size(img, (500, 500), FitSizeMode.INSIDE)
        frames: List[IMG] = [img]

        async def text_frame(text: str, fontsize: int):
            font = await load_font(fontname, fontsize)
            text_w, text_h = font.getsize(text)
            frame = Image.new("RGB", (img_w, text_h + 5), "white")
            await draw_text(
                frame, ((img_w - text_w) / 2, 0), text, font=font, fill="black"
            )
            frames.append(frame)

        for a in args:
            await text_frame(a, min_fontsize)

        frame = Image.new("RGB", (img_w, sum((f.height for f in frames)) + 10), "white")
        current_h = 0
        for f in frames:
            frame.paste(f, (0, current_h))
            current_h += f.height
        return frame

    return await make_jpg_or_gif(img, make)


async def petpet(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = square(users[0].img)
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
    self_head = resize(circle(self_img), (40, 40))
    user_head = resize(circle(user_img), (50, 50))
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
        frame.paste(user_head, user_locs[i], mask=user_head)
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
    img = square(users[0].img)
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
    img = square(users[0].img)
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
) -> BytesIO:
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
    left = rotate(fit_size(user_img, (385, 385)), 24)
    right = rotate(fit_size(user_img, (385, 385)), -11)
    frame.paste(left, (-5, 355))
    frame.paste(right, (649, 310))
    frame.paste(fit_size(self_img, (230, 230)), (408, 418))
    frame.paste(rip, mask=rip)

    if text:
        fontname = BOLD_FONT
        fontsize = await fit_font_size(text, rip.width - 50, 300, fontname, 150, 25)
        if not fontsize:
            raise ValueError(TEXT_TOO_LONG)
        font = await load_font(fontname, fontsize)
        text_w = font.getsize(text)[0]
        await draw_text(
            frame,
            ((rip.width - text_w) / 2, 40),
            text,
            font=font,
            fill="#FF0000",
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
    img = rotate(fit_size(img, (815, 815)), 23)
    frame.paste(img, (-172, -17))
    frame.paste(support, mask=support)
    return save_jpg(frame)


async def always(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img

    async def make(img: IMG) -> IMG:
        img_big = limit_size(img, (500, 0))
        img_small = limit_size(img, (100, 0))
        h1 = img_big.height
        h2 = max(img_small.height, 80)
        frame = Image.new("RGB", (500, h1 + h2 + 10), "white")
        frame.paste(img_big)
        frame.paste(img_small, (290, h1 + 5))
        font = await load_font(DEFAULT_FONT, 60)
        await draw_text(
            frame, (45, h1 + h2 / 2 - 40), "要我一直        吗", font=font, fill="black"
        )
        return frame

    return await make_jpg_or_gif(img, make)


async def loading(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img

    img_big = to_jpg(img).convert("RGBA")
    img_big = limit_size(img_big, (500, 0))
    mask = Image.new("RGBA", img_big.size, (0, 0, 0, 128))
    img_big.paste(mask, mask=mask)
    h1 = img_big.height
    icon = await load_image("loading/1.png")
    img_big = img_big.filter(ImageFilter.GaussianBlur(radius=3))
    img_big.paste(icon, (200, int(h1 / 2) - 50), mask=icon)

    async def make(img: IMG) -> IMG:
        img_small = limit_size(img, (100, 0))
        h2 = max(img_small.height, 80)
        frame = Image.new("RGB", (500, h1 + h2 + 10), "white")
        frame.paste(img_big)
        frame.paste(img_small, (100, h1 + 5))
        font = await load_font(DEFAULT_FONT, 60)
        await draw_text(frame, (210, h1 + h2 / 2 - 40), "不出来", font=font, fill="black")
        return frame

    return await make_jpg_or_gif(img, make)


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


async def littleangel(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = limit_size(img, (500, 500), FitSizeMode.INSIDE)
    img_w, img_h = img.size

    bg = Image.new("RGB", (600, img_h + 230), (255, 255, 255))
    bg.paste(img, (int(300 - img_w / 2), 110))
    fontname = BOLD_FONT

    font = await load_font(fontname, 48)
    text = "非常可爱！简直就是小天使"
    text_w, _ = font.getsize(text)
    await draw_text(
        bg, (300 - text_w / 2, img_h + 120), text, font=font, fill=(0, 0, 0)
    )

    font = await load_font(fontname, 26)
    ta = "他" if users[0].gender == "male" else "她"
    text = f"{ta}没失踪也没怎么样  我只是觉得你们都该看一下"
    text_w, _ = font.getsize(text)
    await draw_text(
        bg, (300 - text_w / 2, img_h + 180), text, font=font, fill=(0, 0, 0)
    )

    name = (args[0] if args else "") or users[0].name or ta
    text = f"请问你们看到{name}了吗?"
    fontsize = await fit_font_size(text, 560, 110, fontname, 70, 25)
    if not fontsize:
        raise ValueError(NAME_TOO_LONG)

    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize(text)
    x = 300 - text_w / 2
    y = 55 - text_h / 2
    await draw_text(bg, (x, y), text, font=font, fill=(0, 0, 0))
    return save_jpg(bg)


async def dont_touch(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frame = await load_image("dont_touch/0.png")
    frame.paste(fit_size(img, (170, 170)), (23, 231))
    return save_jpg(frame)


async def alike(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frame = await load_image("alike/0.png")
    frame.paste(fit_size(img, (90, 90)), (131, 14))
    return save_jpg(frame)


async def roll(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (210, 210))
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
        frame.paste(rotate(img, a, expand=False), (x, y))
        bg = await load_image(f"roll/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def play_game(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("play_game/1.png")
    text = args[0] if args else "来玩休闲游戏啊"
    fontname = DEFAULT_FONT
    fontsize = await fit_font_size(text, 520, 110, fontname, 35, 25)
    if not fontsize:
        raise ValueError(TEXT_TOO_LONG)
    font = await load_font(fontname, fontsize)
    text_w = font.getsize(text)[0]

    async def make(img: IMG) -> IMG:
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        points = [(0, 5), (227, 0), (216, 150), (0, 165)]
        screen = rotate(perspective(fit_size(img, (220, 160)), points), 9)
        frame.paste(screen, (161, 117))
        frame.paste(bg, mask=bg)

        await draw_text(
            frame,
            (263 - text_w / 2, 430),
            text,
            font=font,
            fill="#000000",
            stroke_fill="#FFFFFF",
            stroke_width=2,
        )
        return frame

    return await make_jpg_or_gif(img, make)


async def worship(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    points = [(0, -30), (135, 17), (135, 145), (0, 140)]
    paint = perspective(fit_size(img, (150, 150)), points)
    frames = []
    for i in range(10):
        frame = Image.new("RGBA", (300, 169), (255, 255, 255, 0))
        frame.paste(paint)
        bg = await load_image(f"worship/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)


async def eat(users: List[UserInfo], **kwargs) -> BytesIO:
    img = fit_size(users[0].img, (32, 32))
    frames = []
    for i in range(3):
        frame = Image.new("RGBA", (60, 67), (255, 255, 255, 0))
        frame.paste(img, (1, 38))
        bg = await load_image(f"eat/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.05)


async def bite(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
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
    frame.paste(fit_size(img, (245, 245)), (224, 46))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def police1(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("police/1.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(rotate(fit_size(img, (60, 75)), 16), (37, 291))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def ask(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = limit_size(img, (640, 0))
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
        raise ValueError(REQUIRE_NAME)

    font = await load_font(BOLD_FONT, 25)
    start_h = img_h - mask_h
    start_w = 30
    text_w = font.getsize(name)[0]
    line_w = text_w + 200
    await draw_text(
        img,
        (start_w + (line_w - text_w) / 2, start_h + 5),
        name,
        font=font,
        fill="orange",
    )
    draw = ImageDraw.Draw(img)
    draw.line(
        (start_w, start_h + 45, start_w + line_w, start_h + 45), fill="orange", width=2
    )
    text_w = font.getsize(f"{name}不知道哦")[0]
    await draw_text(
        img,
        (start_w + (line_w - text_w) / 2, start_h + 50),
        f"{name}不知道哦。",
        font=font,
        fill="white",
    )

    sep_w = 30
    sep_h = 80
    bg = Image.new("RGBA", (img_w + sep_w * 2, img_h + sep_h * 2), "white")
    font = await load_font(DEFAULT_FONT, 35)
    if font.getsize(name)[0] > 600:
        raise ValueError(TEXT_TOO_LONG)
    await draw_text(bg, (sep_w, 10), f"让{name}告诉你吧", font=font, fill="black")
    await draw_text(
        bg, (sep_w, sep_h + img_h + 10), f"啊这，{ta}说不知道", font=font, fill="black"
    )
    bg.paste(img, (sep_w, sep_h))
    return save_jpg(bg)


async def prpr(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("prpr/0.png")

    async def make(img: IMG) -> IMG:
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        points = [(0, 19), (236, 0), (287, 264), (66, 351)]
        screen = perspective(fit_size(img, (330, 330)), points)
        frame.paste(screen, (56, 284))
        frame.paste(bg, mask=bg)
        return frame

    return await make_jpg_or_gif(img, make)


async def twist(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (78, 78))
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
        frame.paste(rotate(img, a, expand=False), (x, y))
        bg = await load_image(f"twist/{i}.png")
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.1)


async def wallpaper(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("wallpaper/0.png")

    async def make(img: IMG) -> IMG:
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame.paste(fit_size(img, (775, 496)), (260, 580))
        frame.paste(bg, mask=bg)
        return frame

    return await make_jpg_or_gif(img, make, gif_zoom=0.5)


async def china_flag(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("china_flag/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(fit_size(img, bg.size))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def make_friend(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = limit_size(img, (1000, 0))
    img_w, img_h = img.size

    bg = await load_image("make_friend/0.png")
    frame = img.copy()
    frame.paste(rotate(limit_size(img, (250, 0)), 9), (743, img_h - 155))
    frame.paste(rotate(resize(square(img), (55, 55)), 9), (836, img_h - 278))
    frame.paste(bg, (0, img_h - 1000), mask=bg)
    font = await load_font(DEFAULT_FONT, 40)

    name = (args[0] if args else "") or users[0].name
    if not name:
        raise ValueError(REQUIRE_NAME)
    text_frame = Image.new("RGBA", (500, 50))
    await draw_text(text_frame, (0, -10), name, font=font, fill="#FFFFFF")
    text_frame = rotate(resize(text_frame, (250, 25)), 9)
    frame.paste(text_frame, (710, img_h - 340), mask=text_frame)
    return save_jpg(frame)


async def back_to_work(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("back_to_work/1.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    new_img = fit_size(img, (220, 310), direction=FitSizeDir.NORTH)
    frame.paste(rotate(new_img, 25), (56, 32))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def perfect(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    frame = await load_image("perfect/0.png")
    new_img = fit_size(img, (310, 460), mode=FitSizeMode.INSIDE)
    frame.paste(new_img, (313, 64), mask=new_img)
    return save_jpg(frame)


async def follow(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
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
        raise ValueError(NAME_TOO_LONG)

    frame = Image.new("RGBA", (300 + text_width + 50, 300), (255, 255, 255, 0))
    frame.paste(img, (50, 50), mask=img)
    text_frame = Image.new("RGBA", (text_width + 50, 300), (255, 255, 255, 0))
    await draw_text(
        text_frame, (0, 135 - text_name_h), text_name, font=font, fill="black"
    )
    await draw_text(text_frame, (0, 145), text_follow, font=font, fill="grey")
    frame.paste(text_frame, (300, 0), mask=text_frame)

    return save_jpg(frame)


async def my_friend(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    if not args:
        raise ValueError(REQUIRE_ARG)
    elif len(args) <= 1:
        name = users[0].name or "朋友"
        texts = args
    else:
        name = args[0] or "朋友"
        texts = args[1:]

    name_font = await load_font(DEFAULT_FONT, 25)
    text_font = await load_font(DEFAULT_FONT, 40)
    name_w, name_h = name_font.getsize(name)
    if name_w >= 700:
        raise ValueError(NAME_TOO_LONG)

    corner1 = await load_image("my_friend/corner1.png")
    corner2 = await load_image("my_friend/corner2.png")
    corner3 = await load_image("my_friend/corner3.png")
    corner4 = await load_image("my_friend/corner4.png")
    label = await load_image("my_friend/2.png")
    img = resize(circle(img), (100, 100))

    async def make_dialog(text: str) -> IMG:
        text = "\n".join(wrap_text(text, text_font, 700))
        text_w, text_h = text_font.getsize_multiline(text)
        box_w = max(text_w, name_w + 15) + 140
        box_h = max(text_h + 103, 150)
        box = Image.new("RGBA", (box_w, box_h))
        box.paste(corner1, (0, 0))
        box.paste(corner2, (0, box_h - 75))
        box.paste(corner3, (text_w + 70, 0))
        box.paste(corner4, (text_w + 70, box_h - 75))
        box.paste(Image.new("RGBA", (text_w, box_h - 40), "#ffffff"), (70, 20))
        box.paste(Image.new("RGBA", (text_w + 88, box_h - 150), "#ffffff"), (27, 75))

        await draw_text(
            box,
            (70, 15 + (box_h - 40 - text_h) / 2),
            text,
            font=text_font,
            fill="#000000",
        )
        dialog = Image.new("RGBA", (box.width + 130, box.height + 60), "#eaedf4")
        dialog.paste(img, (20, 20), mask=img)
        dialog.paste(box, (130, 60), mask=box)
        dialog.paste(label, (160, 25))
        await draw_text(
            dialog, (260, 22 + (35 - name_h) / 2), name, font=name_font, fill="#868894"
        )
        return dialog

    dialogs = [await make_dialog(text) for text in texts]
    frame_w = max((dialog.width for dialog in dialogs))
    frame_h = sum((dialog.height for dialog in dialogs))
    frame = Image.new("RGBA", (frame_w, frame_h), "#eaedf4")
    current_h = 0
    for dialog in dialogs:
        frame.paste(dialog, (0, current_h))
        current_h += dialog.height
    return save_jpg(frame)


async def paint(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("paint/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(rotate(fit_size(img, (117, 135)), 4), (95, 107))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def shock(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (300, 300))
    frames = []
    for i in range(30):
        frames.append(
            rotate(
                motion_blur(img, random.randint(-90, 90), random.randint(0, 90)),
                random.randint(-20, 20),
                expand=False,
            )
        )
    return save_gif(frames, 0.01)


async def coupon(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("coupon/0.png")
    new_img = rotate(resize(circle(img), (60, 60)), 22)
    bg.paste(new_img, (164, 85), mask=new_img)

    font = await load_font(DEFAULT_FONT, 30)
    text_img = Image.new("RGBA", (250, 100))
    text = f"{users[0].name}陪睡券" if not args else args[0]
    text += "\n（永久有效）" if len(args) <= 1 else f"\n{args[1]}"
    text_w = font.getsize_multiline(text)[0]
    if text_w > text_img.width:
        raise ValueError(TEXT_TOO_LONG)

    await draw_text(
        text_img,
        ((text_img.width - text_w) / 2, 0),
        text,
        font=font,
        align="center",
        fill="#000000",
    )
    text_img = rotate(text_img, 22)
    bg.paste(text_img, (94, 108), mask=text_img)
    return save_jpg(bg)


async def listen_music(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = circle(img)
    bg = await load_image("listen_music/0.png")
    frames = []
    for i in range(0, 360, 10):
        frame = Image.new("RGBA", (414, 399))
        temp_img = resize(rotate(img, -i, False), (215, 215))
        frame.paste(temp_img, (100, 100), mask=temp_img)
        frame.paste(bg, (0, 0), mask=bg)
        frames.append(to_jpg(frame))
    return save_gif(frames, 0.05)


async def dianzhongdian(
    users: List[UserInfo], args: List[str] = [], **kwargs
) -> BytesIO:
    img = users[0].img

    if args and args[0] == "彩":
        args = args[1:]
    else:
        img = img.convert("L")
    if not args:
        raise ValueError(REQUIRE_ARG)

    img = limit_size(img, (500, 500), FitSizeMode.INSIDE)
    img_w, img_h = img.size
    frames: List[IMG] = [img]

    async def text_frame(text: str, max_fontsize: int, min_fontsize: int) -> int:
        fontname = DEFAULT_FONT
        fontsize = await fit_font_size(
            text, img_w - 20, img_h, fontname, max_fontsize, min_fontsize
        )
        if not fontsize:
            raise ValueError(TEXT_TOO_LONG)
        font = await load_font(fontname, fontsize)
        text_w, text_h = font.getsize(text)
        frame = Image.new("RGB", (img_w, text_h + 5), "#000000")
        await draw_text(frame, ((img_w - text_w) / 2, 0), text, font=font, fill="white")
        frames.append(frame)
        return fontsize

    fontsize = await text_frame(args[0], 50, 10)
    text = args[1] if len(args) > 1 else await translate(args[0])
    if text:
        fontsize = max(int(fontsize / 2), 10)
        await text_frame(text, fontsize, 10)

    frame = Image.new("RGB", (img_w, sum((f.height for f in frames)) + 10), "#000000")
    current_h = 0
    for f in frames:
        frame.paste(f, (0, current_h))
        current_h += f.height
    return save_jpg(frame)


async def funny_mirror(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (500, 500))
    frames = [img]
    coeffs = [0.01, 0.03, 0.05, 0.08, 0.12, 0.17, 0.23, 0.3, 0.4, 0.6]
    borders = [25, 52, 67, 83, 97, 108, 118, 128, 138, 148]
    for i in range(10):
        new_size = 500 - borders[i] * 2
        frames.append(
            resize(
                cut_size(distort(img, (coeffs[i], 0, 0, 0)), (new_size, new_size)),
                (500, 500),
            )
        )
    frames.extend(frames[::-1])
    return save_gif(frames, 0.05)


async def love_you(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    frames = []
    locs = [(68, 65, 70, 70), (63, 59, 80, 80)]
    for i in range(2):
        heart = await load_image(f"love_you/{i}.png")
        frame = Image.new("RGBA", heart.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(heart, mask=heart)
        frames.append(frame)
    return save_gif(frames, 0.2)


async def symmetric(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = limit_size(img, (500, 500), FitSizeMode.INSIDE)
    img_w, img_h = img.size

    boxes = {
        "left": {
            "mode": Image.FLIP_LEFT_RIGHT,
            "frame_box": (img_w // 2 * 2, img_h),
            "first_box": (0, 0, img_w // 2, img_h),
            "first_position": (0, 0),
            "second_box": (img_w // 2, 0, img_w // 2 * 2, img_h),
            "second_position": (img_w // 2, 0),
        },
        "right": {
            "mode": Image.FLIP_LEFT_RIGHT,
            "frame_box": (img_w // 2 * 2, img_h),
            "first_box": (img_w // 2, 0, img_w // 2 * 2, img_h),
            "first_position": (img_w // 2, 0),
            "second_box": (0, 0, img_w // 2, img_h),
            "second_position": (0, 0),
        },
        "top": {
            "mode": Image.FLIP_TOP_BOTTOM,
            "frame_box": (img_w, img_h // 2 * 2),
            "first_box": (0, 0, img_w, img_h // 2),
            "first_position": (0, 0),
            "second_box": (0, img_h // 2, img_w, img_h // 2 * 2),
            "second_position": (0, img_h // 2),
        },
        "bottom": {
            "mode": Image.FLIP_TOP_BOTTOM,
            "frame_box": (img_w, img_h // 2 * 2),
            "first_box": (0, img_h // 2, img_w, img_h // 2 * 2),
            "first_position": (0, img_h // 2),
            "second_box": (0, 0, img_w, img_h // 2),
            "second_position": (0, 0),
        },
    }

    mode = "left"
    if args:
        if "右" in args[0]:
            mode = "right"
        elif "上" in args[0]:
            mode = "top"
        elif "下" in args[0]:
            mode = "bottom"

    first = img
    second = img.transpose(boxes[mode]["mode"])
    frame = Image.new("RGBA", boxes[mode]["frame_box"], (255, 255, 255, 0))

    first = first.crop(boxes[mode]["first_box"])
    frame.paste(first, boxes[mode]["first_position"])
    second = second.crop(boxes[mode]["second_box"])
    frame.paste(second, boxes[mode]["second_position"])

    return save_jpg(frame)


async def safe_sense(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (215, 343))
    frame = await load_image(f"safe_sense/0.png")
    frame.paste(img, (215, 135))

    ta = "她" if users[0].gender == "female" else "他"
    texts = ["你给我的安全感", f"远不及{ta}的万分之一"] if len(args) < 2 else args
    text = "\n".join(texts[:2])

    fontname = DEFAULT_FONT
    fontsize = await fit_font_size(text, 400, 100, fontname, 70, 10)
    if not fontsize:
        raise ValueError(TEXT_TOO_LONG)
    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize_multiline(text)
    await draw_text(
        frame,
        ((frame.width - text_w) / 2, 30 + (45 - text_h) / 2),
        text,
        font=font,
        fill="black",
        align="center",
    )
    return save_jpg(frame)


async def always_like(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    img = users[0].img
    name = (args[0] if args else "") or users[0].name
    if not name:
        raise ValueError(REQUIRE_NAME)
    text = "我永远喜欢" + name
    fontname = BOLD_FONT
    fontsize = await fit_font_size(text, 800, 100, fontname, 70, 30)
    if not fontsize:
        raise ValueError(NAME_TOO_LONG)

    def random_color():
        return random.choice(
            ["red", "darkorange", "gold", "darkgreen", "blue", "cyan", "purple"]
        )

    frame = await load_image(f"always_like/0.png")
    frame.paste(fit_size(img, (350, 400), FitSizeMode.INSIDE), (25, 35))
    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize(text)
    draw = ImageDraw.Draw(frame)
    start_w = (frame.width - text_w) / 2
    start_h = 470 + (100 - text_h) / 2
    await draw_text(frame, (start_w, start_h), text, font=font, fill="black")
    if len(users) > 1:
        line_h = start_h + text_h / 5 * 3
        draw.line(
            (start_w + font.getsize("我永远喜欢")[0], line_h, start_w + text_w, line_h),
            fill=random_color(),
            width=10,
        )

    current_h = start_h
    for i, user in enumerate(users[1:], start=1):
        img = to_jpg(user.img).convert("RGBA")
        new_img = fit_size(img, (350, 400), FitSizeMode.INSIDE)
        frame.paste(
            new_img,
            (10 + random.randint(0, 50), 20 + random.randint(0, 70)),
            mask=new_img,
        )
        name = (args[i] if len(args) > i else "") or user.name
        if not name:
            raise ValueError("找不到对应的名字，名字数须与目标数一致")
        fontsize = await fit_font_size(name, 400, 100, fontname, 70, 30)
        if not fontsize:
            raise ValueError(NAME_TOO_LONG)
        font = await load_font(fontname, fontsize)
        text_w, text_h = font.getsize(name)
        current_h -= text_h - 20
        if current_h < 10:
            raise ValueError("你喜欢的人太多啦")
        start_w = 400 + (430 - text_w) / 2
        await draw_text(frame, (start_w, current_h), name, font=font, fill="black")
        if len(users) > i + 1:
            line_h = current_h + text_h / 5 * 3
            draw.line(
                (start_w, line_h, start_w + text_w, line_h),
                fill=random_color(),
                width=10,
            )
    return save_jpg(frame)


async def interview(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    if len(users) >= 2:
        self_img = users[0].img
        user_img = users[1].img
    else:
        self_img = to_jpg(await load_image("interview/huaji.png"))
        user_img = users[0].img
    self_img = fit_size(self_img, (124, 124))
    user_img = fit_size(user_img, (124, 124))

    frame = Image.new("RGB", (600, 310), "white")
    microphone = await load_image("interview/microphone.png")
    frame.paste(microphone, (330, 103), mask=microphone)
    frame.paste(self_img, (419, 40))
    frame.paste(user_img, (57, 40))

    text = args[0] if args else "采访大佬经验"
    fontname = DEFAULT_FONT
    fontsize = await fit_font_size(text, 550, 100, fontname, 50, 20)
    if not fontsize:
        raise ValueError(TEXT_TOO_LONG)
    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize(text)
    await draw_text(
        frame,
        ((600 - text_w) / 2, 200 + (100 - text_h) / 2),
        text,
        font=font,
        fill="black",
    )
    return save_jpg(frame)


async def punch(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = limit_size(img, (260, 230))
    x = int((260 - img.width) / 2)
    y = int((230 - img.height) / 2)
    frames = []
    # fmt: off
    locs = [
        (-50, 20), (-40, 10), (-30, 0), (-20, -10), (-10, -10), (0, 0),
        (10, 10), (20, 20), (10, 10), (0, 0), (-10, -10), (10, 0), (-30, 10)
    ]
    # fmt: on
    for i in range(13):
        frame = Image.new("RGBA", (260, 230), (255, 255, 255, 0))
        dx, dy = locs[i]
        frame.paste(img, (x + dx, y + dy))
        fist = await load_image(f"punch/{i}.png")
        frame.paste(fist, mask=fist)
        frames.append(frame)
    return save_gif(frames, 0.03)


async def cyan(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (500, 500))
    color = (78, 114, 184)
    img = color_mask(img, color)
    font = await load_font(BOLD_FONT, 80)
    await draw_text(
        img,
        (400, 50),
        "群\n青",
        font=font,
        fill="white",
        stroke_width=2,
        stroke_fill=color,
    )
    font = await load_font(DEFAULT_FONT, 40)
    await draw_text(
        img,
        (310, 270),
        "YOASOBI",
        font=font,
        fill="white",
        stroke_width=2,
        stroke_fill=color,
    )
    return save_jpg(img)


async def pound(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    # fmt: off
    locs = [
        (135, 240, 138, 47), (135, 240, 138, 47), (150, 190, 105, 95), (150, 190, 105, 95),
        (148, 188, 106, 98), (146, 196, 110, 88), (145, 223, 112, 61), (145, 223, 112, 61)
    ]
    # fmt: on
    frames = []
    for i in range(8):
        bg = await load_image(f"pound/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.05)


async def thump(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    # fmt: off
    locs = [(65, 128, 77, 72), (67, 128, 73, 72), (54, 139, 94, 61), (57, 135, 86, 65)]
    # fmt: on
    frames = []
    for i in range(4):
        bg = await load_image(f"thump/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)


async def need(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("need/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(fit_size(img, (115, 115)), (327, 232))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def cover_face(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("cover_face/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    points = [(15, 11), (448, 0), (445, 452), (0, 461)]
    screen = perspective(fit_size(img, (450, 450)), points)
    frame.paste(screen, (120, 154))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def knock(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    # fmt: off
    locs = [(60, 308, 210, 195), (60, 308, 210, 198), (45, 330, 250, 172), (58, 320, 218, 180),
            (60, 310, 215, 193), (40, 320, 250, 285), (48, 308, 226, 192), (51, 301, 223, 200)]
    # fmt: on
    frames = []
    for i in range(8):
        bg = await load_image(f"knock/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)


async def garbage(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (79, 79))
    # fmt: off
    locs = (
        [] + [(39, 40)] * 3 + [(39, 30)] * 2 + [(39, 32)] * 10
        + [(39, 30), (39, 27), (39, 32), (37, 49), (37, 64),
           (37, 67), (37, 67), (39, 69), (37, 70), (37, 70)]
    )
    # fmt: on
    frames = []
    for i in range(25):
        bg = await load_image(f"garbage/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame.paste(img, locs[i])
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.04)


async def whyatme(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("whyatme/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(fit_size(img, (265, 265)), (42, 13))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def decent_kiss(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("decent_kiss/0.png")
    frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
    frame.paste(fit_size(img, (589, 340)), (0, 91))
    frame.paste(bg, mask=bg)
    return save_jpg(frame)


async def jiujiu(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (75, 51))
    frames = []
    for i in range(8):
        bg = await load_image(f"jiujiu/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame.paste(img)
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.06)


async def suck(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    # fmt: off
    locs = [(82, 100, 130, 119), (82, 94, 126, 125), (82, 120, 128, 99), (81, 164, 132, 55),
            (79, 163, 132, 55), (82, 140, 127, 79), (83, 152, 125, 67), (75, 157, 140, 62),
            (72, 165, 144, 54), (80, 132, 128, 87), (81, 127, 127, 92), (79, 111, 132, 108)]
    # fmt: on
    frames = []
    for i in range(12):
        bg = await load_image(f"suck/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.08)


async def hammer(users: List[UserInfo], **kwargs) -> BytesIO:
    img = square(users[0].img)
    # fmt: off
    locs = [(62, 143, 158, 113), (52, 177, 173, 105), (42, 192, 192, 92), (46, 182, 184, 100),
            (54, 169, 174, 110), (69, 128, 144, 135), (65, 130, 152, 124)]
    # fmt: on
    frames = []
    for i in range(7):
        bg = await load_image(f"hammer/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.07)


async def tightly(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (640, 400))
    # fmt: off
    locs = [(39, 169, 267, 141), (40, 167, 264, 143), (38, 174, 270, 135), (40, 167, 264, 143), (38, 174, 270, 135),
            (40, 167, 264, 143), (38, 174, 270, 135), (40, 167, 264, 143), (38, 174, 270, 135), (28, 176, 293, 134),
            (5, 215, 333, 96), (10, 210, 321, 102), (3, 210, 330, 104), (4, 210, 328, 102), (4, 212, 328, 100),
            (4, 212, 328, 100), (4, 212, 328, 100), (4, 212, 328, 100), (4, 212, 328, 100), (29, 195, 285, 120)]
    # fmt: on
    frames = []
    for i in range(20):
        bg = await load_image(f"tightly/{i}.png")
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        x, y, w, h = locs[i]
        frame.paste(resize(img, (w, h)), (x, y))
        frame.paste(bg, mask=bg)
        frames.append(frame)
    return save_gif(frames, 0.08)


async def distracted(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    img = fit_size(img, (500, 500))
    color_mask = await load_image("distracted/1.png")
    img.paste(color_mask, (0, 0), mask=color_mask)
    frame = await load_image("distracted/0.png")
    img.paste(frame, (140, 320), mask=frame)
    return save_jpg(img)


async def anyasuki(users: List[UserInfo], args: List[str] = [], **kwargs) -> BytesIO:
    # Image
    img = users[0].img
    bg = await load_image("anyasuki/1.png")
    # Text
    fontname = DEFAULT_FONT
    text = args[0] if args else "阿尼亚喜欢这个"
    fontsize = await fit_font_size(text, 450, 40, fontname, 40, 10)
    if not fontsize:
        raise ValueError(TEXT_TOO_LONG)
    font = await load_font(fontname, fontsize)
    text_w, text_h = font.getsize(text)
    # Draw
    async def make(img: IMG) -> IMG:
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame_w, frame_h = frame.size
        frame.paste(fit_size(img, (305, 235)), (106, 72))
        frame.paste(bg, mask=bg)
        await draw_text(
            frame,
            ((frame_w - text_w) / 2, frame_h - text_h / 2 - 22),
            text,
            font=font,
            fill="white",
            stroke_fill="black",
            stroke_width=1,
        )
        return frame

    return await make_jpg_or_gif(img, make)


async def thinkwhat(users: List[UserInfo], **kwargs) -> BytesIO:
    img = users[0].img
    bg = await load_image("thinkwhat/0.png")

    async def make(img: IMG) -> IMG:
        frame = Image.new("RGBA", bg.size, (255, 255, 255, 0))
        frame.paste(fit_size(img, (534, 493)), (530, 0))
        frame.paste(bg, mask=bg)
        return frame

    return await make_jpg_or_gif(img, make)
