import datetime as dt
import statistics
import typing as tp

from vkapi.friends import get_friends


def age_predict(user_id: int) -> tp.Optional[float]:
    """
    Наивный прогноз возраста пользователя по возрасту его друзей.

    Возраст считается как медиана среди возраста всех друзей пользователя

    :param user_id: Идентификатор пользователя.
    :return: Медианный возраст пользователя.
    """
    friends = get_friends(user_id, fields=["bdate"], ).items
    list_bdate = [friend.get("bdate", None) for friend in friends]

    friends_count = 0
    sum_age = 0

    for bdate in list_bdate:
        try:
            date = dt.datetime.strptime(bdate.replace(".", " "), "%d %m %Y").date()

        except (ValueError, AttributeError):
            continue
        else:
            friends_count += 1
            age = (dt.datetime.now().date() - date).days // 365
            sum_age += age

    if friends_count != 0:
        return sum_age / friends_count
    else:
        return None
