import typing as tp

import requests
from requests.adapters import HTTPAdapter, Retry


class Session:
    """
    Сессия.

    :param base_url: Базовый адрес, на который будут выполняться запросы.
    :param timeout: Максимальное время ожидания ответа от сервера.
    :param max_retries: Максимальное число повторных запросов.
    :param backoff_factor: Коэффициент экспоненциального нарастания задержки.
    """

    def __init__(
        self,
        base_url: str,
        timeout: float = 5.0,
        max_retries: int = 3,
        backoff_factor: float = 0.3,
    ) -> None:
        self.http = requests.Session()
        self.timeout = timeout
        self.base_url = base_url

        retry_strategy = Retry(
            backoff_factor=backoff_factor,
            total=max_retries,
            status_forcelist=[500, 502, 503, 504],
        )

        adapter = HTTPAdapter(max_retries=retry_strategy)

        self.http.mount(prefix="https://", adapter=adapter)

    def get(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        url = f"{self.base_url}/{url}"
        response = self.http.get(url=url, params=kwargs, timeout=self.timeout)
        return response

    def post(self, url: str, *args: tp.Any, **kwargs: tp.Any) -> requests.Response:
        url = f"{self.base_url}/{url}"
        response = self.http.post(url=url, data=kwargs, timeout=self.timeout)

        return response
