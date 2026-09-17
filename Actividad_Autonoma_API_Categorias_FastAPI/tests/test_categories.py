import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import categories_db

INITIAL_CATEGORIES = [
    {"id": 1, "name": "Computadores", "description": "Equipos de cómputo", "active": True},
    {"id": 2, "name": "Celulares", "description": "Teléfonos inteligentes", "active": True},
    {"id": 3, "name": "Audio", "description": "Audífonos y parlantes", "active": False}
]


@pytest.fixture(autouse=True)
def reset_db():
    categories_db.clear()
    categories_db.extend([cat.copy() for cat in INITIAL_CATEGORIES])


client = TestClient(app)


# CA01: Listar categorías
def test_ca01_list_categories():
    response = client.get("/categories")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 3


# CA02: Consultar existente
def test_ca02_get_existing_category():
    response = client.get("/categories/1")
    assert response.status_code == 200
    assert response.json()["id"] == 1


# CA03: Consultar inexistente
def test_ca03_get_non_existing_category():
    response = client.get("/categories/999")
    assert response.status_code == 404


# CA04: ID inválido
def test_ca04_get_invalid_id():
    response = client.get("/categories/abc")
    assert response.status_code == 422


# CA05: Crear válida
def test_ca05_create_valid_category():
    payload = {"name": "Televisores", "description": "Pantallas Smart TV", "active": True}
    response = client.post("/categories", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Televisores"
    assert "id" in data


# CA06: Nombre demasiado corto
def test_ca06_create_short_name():
    payload = {"name": "TV"}
    response = client.post("/categories", json=payload)
    assert response.status_code == 422


# CA07: Falta nombre
def test_ca07_create_missing_name():
    payload = {"description": "Sin nombre"}
    response = client.post("/categories", json=payload)
    assert response.status_code == 422


# CA08: Actualizar existente
def test_ca08_update_existing_category():
    payload = {"name": "Computadores Laptops"}
    response = client.patch("/categories/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Computadores Laptops"


# CA09: Actualizar inexistente
def test_ca09_update_non_existing_category():
    payload = {"name": "Nuevo Nombre"}
    response = client.patch("/categories/999", json=payload)
    assert response.status_code == 404


# CA10: Eliminar existente
def test_ca10_delete_existing_category():
    response = client.delete("/categories/1")
    assert response.status_code == 204
    assert client.get("/categories/1").status_code == 404


# CA11: Eliminar inexistente
def test_ca11_delete_non_existing_category():
    response = client.delete("/categories/999")
    assert response.status_code == 404


# CA12: Filtrar activas
def test_ca12_filter_active_categories():
    response = client.get("/categories?active=true")
    assert response.status_code == 200
    data = response.json()
    assert all(cat["active"] is True for cat in data)
    assert len(data) == 2


# Reto Opcional: Búsqueda por nombre
def test_reto_search_by_name():
    response = client.get("/categories?search=comp")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Computadores"


def test_reto_search_case_insensitive():
    response = client.get("/categories?search=CELU")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == "Celulares"