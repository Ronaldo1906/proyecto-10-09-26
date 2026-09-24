# API REST de Categorías - FastAPI

API REST autónoma para la gestión de categorías en una tienda tecnológica.

## Instrucciones de Ejecución

1. Activar el entorno virtual e instalar dependencias:
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload

2. iniciar test:

cd proyecto_ejemplo
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install pytest httpx
python -m pytest -v

python -m pytest tests/test_categories.py -v
python -m pytest -k test_ca01_list_categories
python -m pytest -k "test_ca01_list_categories" -v