import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

# CP-CAT-01: Crear categoría válida
def test_cp_cat_01_create_category_valid():
    response = client.post("/categories", json={"name": "Perifericos"})
    assert response.status_code in (201, 200)

# CP-CAT-02: Listar categorías
def test_cp_cat_02_get_categories():
    response = client.get("/categories")
    assert response.status_code == 200

# CP-CAT-04: Consultar categoría inexistente
def test_cp_cat_04_get_unknown_category():
    response = client.get("/categories/99999")
    assert response.status_code == 404

# CP-CAT-05: Nombre demasiado corto
def test_cp_cat_05_category_name_too_short():
    response = client.post("/categories", json={"name": "AB"})
    assert response.status_code == 422

# CP-CAT-06: Nombre exactamente 3 caracteres
def test_cp_cat_06_category_name_min_length():
    response = client.post("/categories", json={"name": "Red"})
    assert response.status_code in (201, 200)

# CP-CAT-07: Nombre duplicado (case insensitive)
def test_cp_cat_07_duplicate_category():
    client.post("/categories", json={"name": "Audio"})
    response = client.post("/categories", json={"name": "audio"})
    assert response.status_code in (409, 422, 400)
