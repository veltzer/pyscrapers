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
    session = ExtSession(base="https://www.instagram.com")
    response = session.ext_get(ConfigUser.user)
    response.save_text()
