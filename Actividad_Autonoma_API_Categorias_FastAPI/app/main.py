from fastapi import FastAPI, HTTPException, status, Query, Response
from typing import Optional, List
from app.schemas import Category, CategoryCreate, CategoryUpdate
from app.database import categories_db

app = FastAPI(
    title="API de Categorías",
    description="API REST autónoma para la gestión de categorías de productos",
    version="1.0.0"
)


@app.get("/categories", response_model=List[Category], status_code=status.HTTP_200_OK)
def get_categories(
    active: Optional[bool] = Query(None),
    search: Optional[str] = Query(None)  # Reto Opcional
):
    result = categories_db
    
    if active is not None:
        result = [cat for cat in result if cat["active"] == active]
        
    if search:
        result = [cat for cat in result if search.lower() in cat["name"].lower()]
        
    return result


@app.get("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def get_category(category_id: int):
    category = next((cat for cat in categories_db if cat["id"] == category_id), None)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    return category


@app.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
def create_category(category_in: CategoryCreate):
    new_id = max([cat["id"] for cat in categories_db], default=0) + 1
    new_category = {
        "id": new_id,
        **category_in.model_dump()
    }
    categories_db.append(new_category)
    return new_category


@app.patch("/categories/{category_id}", response_model=Category, status_code=status.HTTP_200_OK)
def update_category(category_id: int, category_in: CategoryUpdate):
    category = next((cat for cat in categories_db if cat["id"] == category_id), None)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    update_data = category_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        category[key] = value
        
    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: int):
    category = next((cat for cat in categories_db if cat["id"] == category_id), None)
    if not category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Categoría no encontrada"
        )
    
    categories_db.remove(category)
    return Response(status_code=status.HTTP_204_NO_CONTENT)