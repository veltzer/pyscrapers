""" netflix.py """


from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from logging import Logger

    from requests.sessions import Session


def netflix_download(_session: Session, _logger: Logger) -> None:
    """
    This does the downloads
    :param session:
    :param logger:
    :return:
    """
