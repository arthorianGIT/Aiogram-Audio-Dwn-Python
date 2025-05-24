import yt_dlp
import asyncio
from re import sub
from io import BytesIO
import aiohttp
from PIL import Image

async def download_info(url):
    info = await asyncio.to_thread(yt_dlp.YoutubeDL().extract_info, url, download=False)
    return info['title'], info['uploader'], info['upload_date']

async def download_audio(url, kbps):
    info = await asyncio.to_thread(yt_dlp.YoutubeDL().extract_info, url, download=False)
    cleaned_name = sub('[<>|?*&$;#@!№"/`~:.]', '_', info['title'])
    async with aiohttp.ClientSession() as session:
        async with session.get(info['thumbnail']) as response:
            template_data = await response.read()
            template_io = BytesIO(template_data)
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': f'E:/test_videos_audios/{cleaned_name}',
        'quiet': False,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': kbps
        }]
    }
    await asyncio.to_thread(yt_dlp.YoutubeDL(ydl_opts).download, [url])
    image = Image.open(template_io)
    image = image.convert('RGB')
    image.save(f'E:/test_videos_audios/{cleaned_name}.jpeg', format='JPEG', quality=75)
    return cleaned_name