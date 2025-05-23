from dataclasses import dataclass
import asyncpg


@dataclass
class ItemEntry:
    item_id: int
    user_id: int
    title: str
    description: str

    def get_values(self):
        return self.item_id, self.user_id, self.title, self.description


class ItemStorage:
    def __init__(self):
        self._pool: asyncpg.Pool | None = None

    async def connect(self) -> None:
        # We initialize client here, because we need to connect it,
        # __init__ method doesn't support awaits.
        #
        # Pool will be configured using env variables.
        self._pool = await asyncpg.create_pool()

    async def disconnect(self) -> None:
        # Connections should be gracefully closed on app exit to avoid
        # resource leaks.
        await self._pool.close()

    async def create_tables_structure(self) -> None:
        """
        Создайте таблицу items со следующими колонками:
         item_id (int) - обязательное поле, значения должны быть уникальными
         user_id (int) - обязательное поле
         title (str) - обязательное поле
         description (str) - обязательное поле
        """
        # In production environment we will use migration tool
        # like https://github.com/pressly/goose
        # YOUR CODE GOES HERE
        await self._pool.execute("""
            CREATE TABLE items (
                item_id BIGINT UNIQUE NOT NULL,
                user_id BIGINT NOT NULL,
                title TEXT NOT NULL,
                description TEXT NOT NULL
            );
        """)

    async def save_items(self, items: list[ItemEntry]) -> None:
        """
        Напишите код для вставки записей в таблицу items одним запросом, цикл
        использовать нельзя.
        """
        # Don't use str-formatting, query args should be escaped to avoid
        # sql injections https://habr.com/ru/articles/148151/.
        # YOUR CODE GOES HERE
        await self._pool.executemany(
            """
            INSERT INTO items (item_id, user_id, title, description)
            VALUES ($1, $2, $3, $4);
        """,
            map(lambda item: item.get_values(), items),
        )

    async def find_similar_items(
        self, user_id: int, title: str, description: str
    ) -> list[ItemEntry]:
        """
        Напишите код для поиска записей, имеющих указанные user_id, title и description.
        """
        # YOUR CODE GOES HERE
        results = await self._pool.fetch(
            """
            SELECT * FROM items
            WHERE user_id = $1 AND title = $2 AND description = $3;
        """,
            user_id,
            title,
            description,
        )
        return list(map(lambda x: ItemEntry(*x), results))
