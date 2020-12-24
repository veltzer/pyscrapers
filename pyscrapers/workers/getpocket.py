from logging import Logger
from requests.sessions import Session


def getpocket_download(session: Session, _logger: Logger):
    """
    This does the heavy lifting
    :param session:
    :param _logger:
    :return:
    """
    headers = {
        "Origin": "https://app.getpocket.com",  # checked that this is needed
    }
    params = {
        "enable_cors": "1",  # checked that this is needed
        "consumer_key": "78809-9423d8c743a58f62b23ee85c",  # checked that this is needed
    }
    url = "https://getpocket.com/v3/get"
    response = session.post(url=url, headers=headers, params=params)
    response.raise_for_status()
    obj = response.json()
    print(obj)
