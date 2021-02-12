"""
Module that handles the interaction with the youtube_dl library

References:
- https://github.com/ytdl-org/youtube-dl/blob/master/README.md#embedding-youtube-dl
- https://github.com/ytdl-org/youtube-dl/blob/3e4cedf9e8cd3157df2457df7274d0c842421945/youtube_dl/YoutubeDL.py#L137-L312
"""
import logging
from typing import List

import youtube_dl

from pyscrapers.configs import ConfigYoutubeDl, ConfigUrl, ConfigDownload
from pyscrapers.static import LOGGER_NAME


class MyLogger:
    def debug(self, msg):
        pass

    def warning(self, msg):
        pass

    # noinspection PyMethodMayBeStatic
    def error(self, msg):
        print(msg)


def youtube_dl_handler() -> None:
    youtube_dl_download_url(ConfigUrl.url)


def youtube_dl_download_url(url: str) -> None:
    youtube_dl_download_urls([url])


def youtube_dl_download_urls(urls: List[str]) -> None:
    if not ConfigDownload.download:
        return
    logger = logging.getLogger(LOGGER_NAME)
    # all options are here:
    # https://github.com/ytdl-org/youtube-dl/blob/master/youtube_dl/YoutubeDL.py#L128-L278
    ydl_opts = {
        'format': 'bestaudio/best',
        # this shuts everything down
        # 'logger': logger,
        'nooverwrites': True,
        'ignoreerrors': True,
        'restrict'
        # 'hls_prefer_native': True,
        'fixup': 'never',
        # why is this 'outtmpl' here and 'output' on the cmd line?
        "outtmpl": "%(title).100s-%(id)s.%(ext)s",
    }
    logger.debug(f"passing options {ydl_opts}")
    if ConfigYoutubeDl.use_archive:
        ydl_opts['download_archive'] = ConfigYoutubeDl.archive_file
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download(urls)
