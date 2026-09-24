from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional


class CategoryBase(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    active: bool = True

    # Validador para impedir nombres compuestos solo por espacios en blanco
    @field_validator("name")
    @classmethod
    def validate_name_not_whitespace(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("El nombre no puede contener únicamente espacios en blanco.")
        return v.strip()


class CategoryCreate(CategoryBase):
    pass


class CategoryUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=3, max_length=50)
    description: Optional[str] = Field(None, max_length=200)
    active: Optional[bool] = None

    @field_validator("name")
    @classmethod
    def validate_name_not_whitespace(cls, v: Optional[str]) -> Optional[str]:
        if v is not None:
            if not v.strip():
                raise ValueError("El nombre no puede contener únicamente espacios en blanco.")
            return v.strip()
        return v


class Category(CategoryBase):
    id: int

    # Configuración de Pydantic v2 (reemplaza 'class Config:')
    model_config = ConfigDict(from_attributes=True)