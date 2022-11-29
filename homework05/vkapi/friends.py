import dataclasses
import math
import time
import typing as tp

from vkapi import session
from vkapi.config import VK_CONFIG
from vkapi.exceptions import APIError

QueryParams = tp.Optional[tp.Dict[str, tp.Union[str, int]]]


@dataclasses.dataclass(frozen=True)
class FriendsResponse:
    count: int
    items: tp.Union[tp.List[int], tp.List[tp.Dict[str, tp.Any]]]


def get_friends(
        user_id: int, count: int = 5000, offset: int = 0, fields: tp.Optional[tp.List[str]] = None
) -> FriendsResponse:
    """
    Получить список идентификаторов друзей пользователя или расширенную информацию
    о друзьях пользователя (при использовании параметра fields).

    :param user_id: Идентификатор пользователя, список друзей для которого нужно получить.
    :param count: Количество друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества друзей.
    :param fields: Список полей, которые нужно получить для каждого пользователя.
    :return: Список идентификаторов друзей пользователя или список пользователей.
    """
    response = session.get(
        "friends.get",
        user_id=user_id,
        count=count,
        fields=fields,
        offset=offset,
        access_token=VK_CONFIG["access_token"],
        v=VK_CONFIG["version"],
    )

    json = response.json()["response"]
    return FriendsResponse(**json)


class MutualFriends(tp.TypedDict):
    id: int
    common_friends: tp.List[int]
    common_count: int


def get_mutual(
        source_uid: tp.Optional[int] = None,
        target_uid: tp.Optional[int] = None,
        target_uids: tp.Optional[tp.List[int]] = None,
        order: str = "",
        count: tp.Optional[int] = None,
        offset: int = 0,
        progress=None,
) -> tp.Union[tp.List[int], tp.List[MutualFriends]]:
    """
    Получить список идентификаторов общих друзей между парой пользователей.

    :param source_uid: Идентификатор пользователя, чьи друзья пересекаются с друзьями пользователя с идентификатором target_uid.
    :param target_uid: Идентификатор пользователя, с которым необходимо искать общих друзей.
    :param target_uids: Cписок идентификаторов пользователей, с которыми необходимо искать общих друзей.
    :param order: Порядок, в котором нужно вернуть список общих друзей.
    :param count: Количество общих друзей, которое нужно вернуть.
    :param offset: Смещение, необходимое для выборки определенного подмножества общих друзей.
    :param progress: Callback для отображения прогресса.
    """
    if target_uids:
        friends = []
        for iter in range(math.ceil(len(target_uids) / 100)):
            response = session.get(
                "friends.getMutual",
                source_uid=source_uid,
                target_uid=target_uid,
                target_uids=target_uids,
                count=count,
                order=order,
                offset=iter * 100,
                progress=progress,
                access_token=VK_CONFIG["access_token"],
                v=VK_CONFIG["version"],
            )
            friends += response.json()["response"]
            time.sleep(0.35)
        return friends
    else:
        friends = session.get(
            "friends.getMutual",
            source_uid=source_uid,
            target_uid=target_uid,
            count=count,
            offset=offset,
            order=order,
            access_token=VK_CONFIG["access_token"],
            v=VK_CONFIG["version"],
        )
        return friends.json()["response"]



if __name__ == "__main__":
    print(get_mutual(source_uid=214794636, target_uids=[252122581]))
