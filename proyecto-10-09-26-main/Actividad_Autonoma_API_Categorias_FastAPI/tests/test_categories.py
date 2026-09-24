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


# PRUEBA PARAMETRIZADA 1: Manejo de Recursos Inexistentes (404 Not Found)
# Reemplaza y agrupa: CA03, CA09 y CA11
@pytest.mark.parametrize("method, endpoint, payload", [
    ("GET", "/categories/999", None),                      # CA03: Consultar inexistente
    ("PATCH", "/categories/999", {"name": "Nuevo Nombre"}), # CA09: Actualizar inexistente
    ("DELETE", "/categories/999", None),                   # CA11: Eliminar inexistente
])
def test_non_existing_category_operations(method, endpoint, payload):
    if method == "GET":
        response = client.get(endpoint)
    elif method == "PATCH":
        response = client.patch(endpoint, json=payload)
    elif method == "DELETE":
        response = client.delete(endpoint)
    
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


# PRUEBA PARAMETRIZADA 2: Validaciones de Payload Inválido en Creación (HTTP 422)
# Reemplaza y agrupa: CA06 y CA07
@pytest.mark.parametrize("invalid_payload, description", [
    ({"name": "TV"}, "Nombre demasiado corto (< 3 caracteres)"), # CA06
    ({"description": "Sin nombre"}, "Falta el campo 'name'"),   # CA07
    ({"name": "   "}, "Nombre solo con espacios en blanco"),
])
def test_create_category_invalid_payload(invalid_payload, description):
    response = client.post("/categories", json=invalid_payload)
    assert response.status_code == 422


# CA08: Actualizar existente
def test_ca08_update_existing_category():
    payload = {"name": "Computadores Laptops"}
    response = client.patch("/categories/1", json=payload)
    assert response.status_code == 200
    assert response.json()["name"] == "Computadores Laptops"


# CA10: Eliminar existente
def test_ca10_delete_existing_category():
    response = client.delete("/categories/1")
    assert response.status_code == 204
    assert client.get("/categories/1").status_code == 404


# CA12: Filtrar activas
def test_ca12_filter_active_categories():
    response = client.get("/categories?active=true")
    assert response.status_code == 200
    data = response.json()
    assert all(cat["active"] is True for cat in data)
    assert len(data) == 2


# PRUEBA PARAMETRIZADA 3: Búsquedas por nombre (QueryParams)
# Reemplaza y agrupa: test_reto_search_by_name y test_reto_search_case_insensitive
@pytest.mark.parametrize("search_term, expected_name", [
    ("comp", "Computadores"),  # Búsqueda parcial en minúsculas
    ("CELU", "Celulares"),     # Búsqueda Case-Insensitive en mayúsculas
    ("Audio", "Audio"),        # Búsqueda exacta
])
def test_search_categories_by_name(search_term, expected_name):
    response = client.get(f"/categories?search={search_term}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["name"] == expected_name