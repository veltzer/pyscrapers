from typing import List

import requests

import pyscrapers.core.utils


def scrape_mambaru(user_id: str, cookies) -> List[str]:
    main_url = 'https://www.mamba.ru/{user_id}'.format(user_id=user_id)
    r = requests.get(main_url, cookies=cookies)
    root = pyscrapers.core.utils.get_html_dom_content(r)
    print(root)
    return []
