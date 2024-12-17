from fastapi import status
from httpx import AsyncClient

from app.main import app


async def test_hello_world(client: AsyncClient) -> None:
    response = await client.get(
        app.url_path_for("hello_world"),
    )

    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "Hello, World!"}
