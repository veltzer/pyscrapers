from logging import Logger
from pyscrapers.configs import ConfigUser
from pyscrapers.core.ext_requests import ExtSession


def instagram_stories_download(_session: ExtSession, _logger: Logger):
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    url = f"https://www.instagram.com/{ConfigUser.user}"
    session = ExtSession()
    session.get(url)
