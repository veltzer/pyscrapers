"""
Module that handles the interaction with the youtube_dl library

References:
- https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
"""
import os
from typing import List

import youtube_dl

from pyscrapers.configs import ConfigYoutubeDl, ConfigDownload


class MyLogger(object):
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    # noinspection PyMethodMayBeStatic
    def error(self, msg):
        print(msg)


def youtube_dl_handler() -> None:
    youtube_dl_download_url(ConfigYoutubeDl.url, ConfigDownload.folder)


def youtube_dl_download_url(url: str, folder: str) -> None:
    youtube_dl_download_urls([url], folder)


def youtube_dl_download_urls(urls: List[str], folder: str) -> None:
    ydl_opts = {
        'format': 'bestaudio/best',
        # 'logger': MyLogger(),
        'nooverwrites': True,
        'ignoreerrors': True,
        'outtmpl': os.path.join(folder, '%(title)s-%(id)s.%(ext)s'),
        'download_archive': os.path.expanduser('~/.config/youtube-dl-archive'),
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
