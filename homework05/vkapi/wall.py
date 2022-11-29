import time
import typing as tp
from string import Template

import pandas as pd
from pandas import json_normalize
from vkapi import session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError


def get_posts_2500(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
) -> tp.Dict[str, tp.Any]:
    code = """return API.wall.get({
                '"owner_id": "owner_id"',
                '"domain": "domain"',
                '"offset": offset',
                '"count": "1"',
                '"filter": "filter"',
                '"extended": extended',
                '"fields": "fields"',
                '"v": "v"'
                });"""

    request_data = {
        "access_token": VK_CONFIG["access_token"],
        "v": VK_CONFIG["version"],
        "code": code,
    }
    post = session.post(
        "execute",
        **request_data,
    )

    return post.json()["response"]["items"]


def get_wall_execute(
    owner_id: str = "",
    domain: str = "",
    offset: int = 0,
    count: int = 10,
    max_count: int = 2500,
    filter: str = "owner",
    extended: int = 0,
    fields: tp.Optional[tp.List[str]] = None,
    progress=None,
) -> pd.DataFrame:
    """
    Возвращает список записей со стены пользователя или сообщества.
    @see: https://vk.com/dev/wall.get
    :param owner_id: Идентификатор пользователя или сообщества, со стены которого необходимо получить записи.
    :param domain: Короткий адрес пользователя или сообщества.
    :param offset: Смещение, необходимое для выборки определенного подмножества записей.
    :param count: Количество записей, которое необходимо получить (0 - все записи).
    :param max_count: Максимальное число записей, которое может быть получено за один запрос.
    :param filter: Определяет, какие типы записей на стене необходимо получить.
    :param extended: 1 — в ответе будут возвращены дополнительные поля profiles и groups, содержащие информацию о пользователях и сообществах.
    :param fields: Список дополнительных полей для профилей и сообществ, которые необходимо вернуть.
    :param progress: Callback для отображения прогресса.
    """

    response: tp.List[str] = []
    while count > 0:
        posts = get_posts_2500(
            owner_id, domain, offset, min(count, max_count), max_count, filter, extended, fields
        )
        offset += min(count, max_count)
        count -= max_count
        response += posts
        time.sleep(1)
    return json_normalize(response)
