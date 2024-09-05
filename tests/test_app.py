from http import HTTPStatus

import pytest
from fastapi.testclient import TestClient

from fast_zero.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    response = client.get("/")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "batatinhas fritas"}


def test_create_user(client):
    response = client.post(
        "/users/",
        json={
            "username": "testeusername",
            "password": "testesenha",
            "email": "test@test.com",
        },
    )

    assert response.status_code == HTTPStatus.CREATED
    assert response.json() == {
        "username": "testeusername",
        "email": "test@test.com",
        "id": 1,
    }


def test_read_users(client):
    response = client.get("/users/")

    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "users": [
            {
                "username": "testeusername",
                "email": "test@test.com",
                "id": 1,
            }
        ]
    }


def test_delete_user(client):
    response = client.delete("/users/1")
    assert response.json() == {"message": "User deleted"}


def test_read_user(client):
    # Cria um novo usuário
    response = client.post(
        "/users/",
        json={
            "username": "testeusername2",
            "password": "testesenha2",
            "email": "test2@test.com",
        },
    )

    # Extrai o ID gerado pelo backend
    user_id = response.json()["id"]

    # Adiciona o print para verificar o ID gerado
    print(f"User ID gerado: {user_id}")

    # Faz a requisição GET para pegar o usuário criado
    response = client.get(f"/users/{user_id}")
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {
        "username": "testeusername2",
        "email": "test2@test.com",
        "id": user_id,
    }
