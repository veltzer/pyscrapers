import json

from pyscrapers.core.url_set import UrlSet


def scrape_mambaru(user_id: str, session, url_set: UrlSet) -> None:
    # raise ValueError("mamba still not implemented")
    # main_url = 'https://www.mamba.ru/{user_id}'.format(user_id=user_id)
    main_url = 'https://www.mamba.ru/mobile/api/v5.17.0.0/?reqType=json'
    sys_requests_container = [
        {
            "uri": "/users/{}/albums/workers/".format(user_id),
            "method": "GET",
            "params": {
                "langId": "en",
                "dateType": "timestamp",
                "limit": -1,
            },
        }
    ]
    request_obj = {
        "langId": "en",
        "dateType": "timestamp",
        "limit": 10000,
        "sysRequestsContainer": sys_requests_container,
    }
    response = session.post(main_url, json=request_obj)
    response.raise_for_status()
    response_str = response.content.decode()
    response_obj = json.loads(response_str)
    response_obj = response_obj["sysResponsesContainer"][0]
    for album in response_obj["albums"]:
        for photo in album["workers"]:
            url_set.append(photo["hugePhotoUrl"])
