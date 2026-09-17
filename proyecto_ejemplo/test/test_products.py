import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import products_db

INITIAL_PRODUCTS = [
    {"id": 1, "name": "Product 1", "category": "Laptops", "price": 10.99, "stock": 100, "available": True},
    {"id": 2, "name": "Product 2", "category": "Cameras", "price": 15.99, "stock": 50, "available": True},
    {"id": 3, "name": "Product 3", "category": "Laptops", "price": 20.99, "stock": 0, "available": False},
    {"id": 4, "name": "Product 4", "category": "Cameras", "price": 25.99, "stock": 30, "available": True},
    {"id": 5, "name": "Product 5", "category": "Laptops", "price": 30.99, "stock": 20, "available": True},
]

@pytest.fixture(autouse=True)
def reset_products_db():
    products_db.clear()
    products_db.extend(INITIAL_PRODUCTS)

client = TestClient(app)

# CP014: Verificar health check
def test_cp014_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}

# CP001: Obtener lista completa de productos
def test_cp001_get_products():
    response = client.get("/products/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)

# CP004: Consultar producto por ID existente
def test_cp004_get_existing_product():
    response = client.get("/products/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert "name" in data

# CP005: Consultar producto por ID inexistente
def test_cp005_get_non_existing_product():
    response = client.get("/products/999")
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

# CP006: Consultar producto con ID de tipo inválido
def test_cp006_invalid_product_id():
    response = client.get("/products/abc")
    assert response.status_code == 422
    assert "detail" in response.json()

# CP002: Filtrar productos por disponibilidad
def test_cp002_filter_available_products():
    response = client.get("/products/?available=true")
    assert response.status_code == 200
    data = response.json()
    assert all(product["available"] is True for product in data)

# CP003: Filtrar productos por categoría
def test_cp003_filter_products_by_category():
    response = client.get("/products/?category=Laptops")
    assert response.status_code == 200
    data = response.json()
    assert all(product["category"] == "Laptops" for product in data)

# CP007: Crear producto correctamente
def test_cp007_create_product():
    new_product = {
        "name": "New Product",
        "category": "Electronics",
        "price": 49.99,
        "stock": 10,
        "available": True,
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == new_product["name"]
    assert "id" in data

# CP008: Rechazar creación con precio negativo
def test_cp008_create_product_negative_price():
    new_product = {
        "name": "Invalid Product",
        "category": "Electronics",
        "price": -10.00,
        "stock": 5,
        "available": True,
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 422
    assert "detail" in response.json()

# CP009: Permitir creación con stock igual a cero (Frontera)
def test_cp009_create_product_zero_stock():
    new_product = {
        "name": "Zero Stock Product",
        "category": "Electronics",
        "price": 15.00,
        "stock": 0,
        "available": True,
    }
    response = client.post("/products", json=new_product)
    assert response.status_code == 201
    assert response.json()["stock"] == 0

# CP010: Actualizar producto de forma completa con PUT
def test_cp010_update_product():
    updated_product = {
        "name": "Updated Product",
        "category": "Electronics",
        "price": 99.99,
        "stock": 20,
        "available": False,
    }
    response = client.put("/products/1", json=updated_product)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == updated_product["name"]

# CP011: Actualizar campo específico con PATCH
def test_cp011_update_price_patch():
    updated_price = {"price": 79.99}
    response = client.patch("/products/1", json=updated_price)
    assert response.status_code == 200
    assert response.json()["price"] == 79.99

# CP012: Actualizar producto inexistente
def test_cp012_update_non_existing_product():
    updated_product = {
        "name": "Non-existing Product",
        "category": "Category",
        "price": 99.99,
        "stock": 10,
        "available": True,
    }
    response = client.put("/products/999", json=updated_product)
    assert response.status_code == 404
    assert response.json() == {"detail": "Product not found"}

# CP013: Eliminar producto existente
def test_cp013_delete_product():
    response = client.delete("/products/1")
    assert response.status_code == 204
    get_response = client.get("/products/1")
    assert get_response.status_code == 404