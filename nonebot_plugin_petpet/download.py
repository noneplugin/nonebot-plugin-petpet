import io
import httpx
import hashlib
from pathlib import Path


data_path = Path() / 'data' / 'petpet'


class DownloadError(Exception):
    pass


async def download(url: str) -> bytes:
    async with httpx.AsyncClient() as client:
        for i in range(3):
            try:
                resp = await client.get(url)
                if resp.status_code != 200:
                    continue
                return resp.content
            except:
                pass
        return None


async def get_resource(path: str, name: str) -> io.BytesIO:
    dir_path = data_path / 'resources' / path
    file_path = dir_path / name
    if not file_path.exists():
        dir_path.mkdir(parents=True, exist_ok=True)
        url = f'https://cdn.jsdelivr.net/gh/MeetWq/nonebot-plugin-petpet@main/resources/{path}/{name}'
        data = await download(url)
        if data:
            with file_path.open('wb') as f:
                f.write(data)
    if not file_path.exists():
        raise DownloadError
    with open(file_path, 'rb') as f:
        return io.BytesIO(f.read())


async def get_avatar(user_id: str) -> io.BytesIO:
    url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=640"
    data = await download(url)
    if not data or hashlib.md5(data).hexdigest() == 'acef72340ac0e914090bd35799f5594e':
        url = f"http://q1.qlogo.cn/g?b=qq&nk={user_id}&s=100"
        data = await download(url)
        if not data:
            raise DownloadError
    return io.BytesIO(data)


async def get_image(url: str) -> io.BytesIO:
    data = await download(url)
    if not data:
        raise DownloadError
    return io.BytesIO(data)
