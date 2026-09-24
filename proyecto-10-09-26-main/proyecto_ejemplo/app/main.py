from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI(title="TechStore API")

# --- Base de Datos Temporal en Memoria ---
categories_db = []
products_db = [
    {
        "id": 1,
        "name": "Laptop",
        "category": "Laptops",
        "price": 1200.00,
        "stock": 10,
        "available": True
    }
]
cat_id_counter = 1
prod_id_counter = 2

# --- Schemas ---
class CategoryCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=60)

class CategoryResponse(BaseModel):
    id: int
    name: str

class ProductCreate(BaseModel):
    name: str = Field(..., min_length=3, max_length=80)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)
    category_id: Optional[int] = None

# --- Rutas de Categorías (/categories) ---
@app.post("/categories", response_model=CategoryResponse, status_code=status.HTTP_201_CREATED)
def create_category(category: CategoryCreate):
    global cat_id_counter
    if any(c["name"].lower() == category.name.lower() for c in categories_db):
        raise HTTPException(status_code=409, detail="La categoría ya existe")
    
    new_cat = {"id": cat_id_counter, "name": category.name}
    categories_db.append(new_cat)
    cat_id_counter += 1
    return new_cat

@app.get("/categories", response_model=List[CategoryResponse])
def get_categories():
    return categories_db

@app.get("/categories/{category_id}", response_model=CategoryResponse)
def get_category(category_id: int):
    for cat in categories_db:
        if cat["id"] == category_id:
            return cat
    raise HTTPException(status_code=404, detail="Category not found")

# --- Rutas de Productos (/products & /health) ---
@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/products")
def get_products(available: Optional[bool] = None, category: Optional[str] = None):
    res = products_db
    if available is True:
        res = [p for p in res if p.get("stock", 0) > 0]
    if category:
        res = [p for p in res if p.get("category") == category]
    return res

@app.get("/products/{product_id}")
def get_product(product_id: int):
    for p in products_db:
        if p["id"] == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.post("/products", status_code=status.HTTP_201_CREATED)
def create_product(product: ProductCreate):
    global prod_id_counter
    if product.category_id is not None:
        if not any(c["id"] == product.category_id for c in categories_db):
            raise HTTPException(status_code=404, detail="Category not found")
    
    new_prod = product.model_dump()
    new_prod["id"] = prod_id_counter
    products_db.append(new_prod)
    prod_id_counter += 1
    return new_prod

@app.put("/products/{product_id}")
def update_product(product_id: int, product: ProductCreate):
    for idx, p in enumerate(products_db):
        if p["id"] == product_id:
            updated = product.model_dump()
            updated["id"] = product_id
            products_db[idx] = updated
            return updated
    raise HTTPException(status_code=404, detail="Product not found")

@app.patch("/products/{product_id}")
def patch_product_price(product_id: int, price_data: dict):
    for p in products_db:
        if p["id"] == product_id:
            if "price" in price_data and price_data["price"] > 0:
                p["price"] = price_data["price"]
                return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int):
    for idx, p in enumerate(products_db):
        if p["id"] == product_id:
            products_db.pop(idx)
            return
    raise HTTPException(status_code=404, detail="Product not found")
