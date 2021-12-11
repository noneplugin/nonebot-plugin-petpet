import httpx
import hashlib
from pathlib import Path
from nonebot.log import logger


data_path = Path() / 'data' / 'petpet'


class DownloadError(Exception):
    pass


async def download_image(s: str) -> bytes:
    if s.isdigit():
        return await download_avatar(s)
    else:
        return await download_url(s)


async def download_url(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                return resp.content
            except Exception as e:
                logger.warning(f'Error downloading {url}, retry {i}/3: {e}')
    raise DownloadError


async def get_resource(path: str, name: str) -> bytes:
    dir_path = data_path / 'resources' / path
    file_path = dir_path / name
    if not file_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        url = f'https://cdn.jsdelivr.net/gh/MeetWq/nonebot-plugin-petpet@main/resources/{path}/{name}'
        data = await download_url(url)
        if data:
            with file_path.open('wb') as f:
                f.write(data)
    if not file_path.exists():
        raise DownloadError
    return file_path.read_bytes()


async def download_avatar(user_id: str) -> bytes:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download_url(url)
    if not data or hashlib.md5(data).hexdigest() == 'acef72340ac0e914090bd35799f5594e':
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download_url(url)
        if not data:
            raise DownloadError
    return data
