from typing import List
from pydantic import BaseModel, Extra

from nonebot import get_driver


class Config(BaseModel, extra=Extra.ignore):
    petpet_command_start: List[str] = [""]
    petpet_resource_url: str = "https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-petpet/v0.3.x/resources"
    petpet_disabled_list: List[str] = []
    petpet_gif_max_size: float = 10
    petpet_gif_max_frames: int = 100
    baidu_trans_appid: str = ""
    baidu_trans_apikey: str = ""


petpet_config = Config.parse_obj(get_driver().config.dict())
petpet_config.petpet_resource_url = petpet_config.petpet_resource_url.strip("/")
