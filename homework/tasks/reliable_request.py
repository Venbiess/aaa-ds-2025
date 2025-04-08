import abc
import httpx


class ResultsObserver(abc.ABC):
    _data_observed = []

    @abc.abstractmethod
    def observe(self, data: bytes) -> None:
        self._data_observed.append(data)

    @abc.abstractmethod
    def get_observed_data(self) -> list[bytes]:
        return self._data_observed


async def do_reliable_request(url: str, observer: ResultsObserver) -> None:
    """
    Одна из главных проблем распределённых систем - это ненадёжность связи.

    Ваша задача заключается в том, чтобы таким образом исправить этот код, чтобы он
    умел переживать возвраты ошибок и таймауты со стороны сервера, гарантируя
    успешный запрос (в реальной жизни такая гарантия невозможна, но мы чуть упростим себе задачу).

    Все успешно полученные результаты должны регистрироваться с помощью обсёрвера.
    """
    RETRIES_NUMBER = 5

    async with httpx.AsyncClient() as client:
        # YOUR CODE GOES HERE
        for _ in range(RETRIES_NUMBER):
            try:
                response = await client.get(url, timeout=10)
                response.raise_for_status()
                data = response.read()

                observer.observe(data)
                break
            except TimeoutError:
                continue
            except Exception:
                continue
        return
        #####################
