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
