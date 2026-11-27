""" instagram_stories.py """


from typing import TYPE_CHECKING

from pyscrapers.configs import ConfigUser
from pyscrapers.core.ext_requests import ExtSession

if TYPE_CHECKING:
    from logging import Logger


def instagram_stories_download(_session: ExtSession, _logger: Logger) -> None:
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
    session = ExtSession(base="https://www.instagram.com")
    response = session.ext_get(ConfigUser.user)
    response.save_text()
