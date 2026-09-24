# Plan de Pruebas - TechStore API (Products & Categories)
## 1. Información General
- **Proyecto:** TechStore API (Categorías y Productos)
- **Versión:** 1.0.0
- **Tecnologías:** Python 3.14, FastAPI, Pydantic, Pytest, TestClient
- **Responsable de pruebas:** Aprendiz QA

## 2. Objetivo
Verificar la calidad y estabilidad en la API REST de TechStore, auditando los módulos de Categorías y Productos.

## 3. Alcance
- **Incluido:** Endpoints /categories (EP01-EP03) y /products (EP04-EP08), validaciones Pydantic y códigos HTTP (201, 200, 204, 404, 409, 422).
- **Fuera de alcance:** Autenticación, pruebas de carga e interfaz gráfica (UI).

## 4. Análisis de Riesgos
| Riesgo | Probabilidad | Impacto | Prioridad | Caso Mitigante |
|---|---|---|---|---|
| Categoría duplicada con distinta capitalización | Media | Alto | Alta | CP-CAT-07 |
| Productos con precio <= 0 o stock negativo | Alta | Alto | Alta | CP-PROD-11, CP-PROD-12, CP-PROD-15 |
| Asignación de categoría inexistente a producto | Media | Alto | Alta | CP-PROD-16, CP-PROD-18 |
| Error 500 al consultar/actualizar ID inexistente | Media | Medio | Media | CP-CAT-04, CP-PROD-04, CP-PROD-06 |

## 5. Criterios de Salida
- 100% de cobertura documental de RF01-RF12 y RN01-RN08.
- Mínimo 15 pruebas automatizadas en pytest.
- 0 defectos críticos/altos abiertos.
- Tasa de aprobación >= 90%.
