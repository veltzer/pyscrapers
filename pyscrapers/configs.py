"""
All configurations for pymakehelper
"""


from pytconf.config import Config, ParamCreator

import logging


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
        default=logging.getLevelName(logging.ERROR),

    )


class ConfigDebugRequests(Config):
    """
    Configure how to user the requests module
    """
    debug = ParamCreator.create_bool(
        help_string="Do you want to debug the requests module?",
        default=False,
    )


class ConfigCookiesSource(Config):
    """
    Configure where to get cookies from...
    """
    browser = ParamCreator.create_choice(
        choice_list=["none", "firefox", "chrome"],
        help_string="Which browser to take cookies from?",
        default="firefox",
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
    start = ParamCreator.create_int(
        help_string="start number for image names",
        default=0,
    )

