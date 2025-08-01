"""
All configurations for pyscrapers
"""
import os
import logging

from pytconf import Config, ParamCreator


class ConfigLogging(Config):
    """
    Parameters to control logging
    """
    loglevel = ParamCreator.create_choice(
        choice_list=[
            logging.getLevelName(logging.NOTSET),
            logging.getLevelName(logging.DEBUG),
            logging.getLevelName(logging.INFO),
            logging.getLevelName(logging.WARNING),
            logging.getLevelName(logging.WARN),
            logging.getLevelName(logging.ERROR),
            logging.getLevelName(logging.FATAL),
            logging.getLevelName(logging.CRITICAL),
        ],
        help_string="What log level to use?",
        default=logging.getLevelName(logging.INFO),
    )


class ConfigDebugUrls(Config):
    """
    Configure how to debug urls
    """
    save = ParamCreator.create_bool(
        help_string="Do you want to save urls?",
        default=False,
    )


class ConfigDownload(Config):
    """
    Configure details about the download process
    """
    download_as_collecting = ParamCreator.create_bool(
        help_string="Do you want download while collecting the urls?",
        default=False,
    )
    download = ParamCreator.create_bool(
        help_string="really download or just print the urls?",
        default=True,
    )
    folder = ParamCreator.create_existing_folder(
        help_string="where to save the data to?",
        default=".",
    )


class ConfigCookiesSource(Config):
    """
        Configure where to get cookies from
    """

    browser = ParamCreator.create_choice(
        choice_list=["none", "firefox", "chrome"],
        help_string="Which browser to take cookies from?",
        default="chrome",
    )


class ConfigSiteId(Config):
    """
    Parameters for downloading workers
    """
    site = ParamCreator.create_choice(
        choice_list=["facebook", "instagram", "travelgirls", "vk", "mamba.ru"],
        help_string="Which site to download from?",
    )
    user_id = ParamCreator.create_str(
        help_string="""Which user id to user?
            https://www.facebook.com/profile.php?id=[user_id]
            https://www.instagram.com/[user_id]
            http://www.travelgirls.com/member/[user_id]
            https://vk.com/id[user_id]
            http://www.mamba.ru/mb[user_id]""",
    )


class ConfigUser(Config):
    """
    Parameters for a user
    """
    user = ParamCreator.create_str(
        help_string="Which user id to user?",
    )


class ConfigYoutubeDl(Config):
    """
    Configuration for youtube downloads
    """
    use_archive = ParamCreator.create_bool(
        help_string="Should we use an archive?",
        default=True,
    )
    archive_file = ParamCreator.create_existing_file(
        help_string="What file to use as archive?",
        default=os.path.expanduser('~/.config/youtube-dl-archive'),
    )


class ConfigUrl(Config):
    """
    Parameters for what url to download
    """
    url = ParamCreator.create_str(
        help_string="url to download"
    )


class ConfigRequests(Config):
    """
    Parameters to config the requests module
    """
    connect_timeout = ParamCreator.create_int_or_none(
        help_string="Timeout for connections in seconds (none means endless)",
        default=5,
    )
    read_timeout = ParamCreator.create_int_or_none(
        help_string="Timeout for reading in seconds (none means endless)",
        default=5,
    )
    debug = ParamCreator.create_bool(
        help_string="Do you want to debug the requests module?",
        default=False,
    )
    progress = ParamCreator.create_bool(
        help_string="Do you want to display progress?",
        default=False,
    )
