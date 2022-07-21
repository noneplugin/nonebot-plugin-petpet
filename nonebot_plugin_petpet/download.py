import json
import httpx
import hashlib
import asyncio
from pathlib import Path
from nonebot.log import logger
from nonebot import get_driver

from nonebot_plugin_imageutils import BuildImage
from nonebot_plugin_imageutils.fonts import add_font

data_path = Path() / "data" / "petpet"


def load_image(path: str) -> BuildImage:
    return BuildImage.open(data_path / "images" / path).convert("RGBA")


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url, timeout=20)
                resp.raise_for_status()
                return resp.content
            except Exception as e:
                logger.warning(f"Error downloading {url}, retry {i}/3: {e}")
                await asyncio.sleep(3)
    raise Exception(f"{url} 下载失败！")


async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if hashlib.md5(data).hexdigest() == "acef72340ac0e914090bd35799f5594e":
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
    return data


def resource_url(path: str) -> str:
    return f"https://ghproxy.com/https://raw.githubusercontent.com/noneplugin/nonebot-plugin-petpet/v0.3.x/resources/{path}"


async def download_resource(path: str) -> bytes:
    return await download_url(resource_url(path))


async def check_resources():
    resource_list = json.loads(
        (await download_resource("resource_list.json")).decode("utf-8")
    )
    for resource in resource_list:
        file_name = str(resource["path"])
        file_path = data_path / file_name
        file_hash = str(resource["hash"])
        if (
            file_path.exists()
            and hashlib.md5(file_path.read_bytes()).hexdigest() == file_hash
        ):
            continue
        logger.debug(f"Downloading {file_name} ...")
        file_path.parent.mkdir(parents=True, exist_ok=True)
        try:
            data = await download_resource(file_name)
            with file_path.open("wb") as f:
                f.write(data)
        except Exception as e:
            logger.warning(str(e))
    await add_font("consola.ttf", resource_url("fonts/consola.ttf"))


driver = get_driver()


@driver.on_startup
def _():
    logger.info("正在检查资源文件...")
    asyncio.ensure_future(check_resources())
