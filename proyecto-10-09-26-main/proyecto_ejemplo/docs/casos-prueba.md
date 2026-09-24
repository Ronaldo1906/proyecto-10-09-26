# Casos de Prueba Diseñados (Total: 25)

## Módulo Categorías (7 Casos Guiados)
- **CP-CAT-01:** Crear categoría válida | RF01 | Esperado: HTTP 201 | Estado: PASSED
- **CP-CAT-02:** Listar categorías | RF02 | Esperado: HTTP 200 | Estado: PASSED
- **CP-CAT-03:** Consultar categoría por ID | RF03 | Esperado: HTTP 200 | Estado: PASSED
- **CP-CAT-04:** Consultar categoría inexistente (ID 99999) | RF04 | Esperado: HTTP 404 | Estado: PASSED
- **CP-CAT-05:** Crear categoría con nombre < 3 caracteres | RN01 | Esperado: HTTP 422 | Estado: PASSED
- **CP-CAT-06:** Crear categoría con nombre exactamente 3 caracteres | RN01 | Esperado: HTTP 201 | Estado: PASSED
- **CP-CAT-07:** Rechazar categoría duplicada (Audio / audio) | RN02 | Esperado: HTTP 409 | Estado: PASSED

## Módulo Productos (18 Casos Evaluables)
- **CP-PROD-01:** Crear producto válido asociado a categoría | RF05 | Esperado: HTTP 201 | Estado: PASSED
- **CP-PROD-02:** Listar productos registrados | RF06 | Esperado: HTTP 200 | Estado: PASSED
- **CP-PROD-03:** Consultar producto por ID | RF07 | Esperado: HTTP 200 | Estado: PASSED
- **CP-PROD-04:** Consultar producto inexistente | RF08 | Esperado: HTTP 404 | Estado: PASSED
- **CP-PROD-05:** Actualizar producto con datos válidos | RF09 | Esperado: HTTP 200 | Estado: PASSED
- **CP-PROD-06:** Actualizar producto inexistente | RF10 | Esperado: HTTP 404 | Estado: PASSED
- **CP-PROD-07:** Eliminar producto existente | RF11 | Esperado: HTTP 204 | Estado: PASSED
- **CP-PROD-08:** Eliminar producto inexistente | RF12 | Esperado: HTTP 404 | Estado: PASSED
- **CP-PROD-09:** Producto con nombre < 3 caracteres | RN03 | Esperado: HTTP 422 | Estado: PASSED
- **CP-PROD-10:** Producto con nombre de 3 caracteres | RN03 | Esperado: HTTP 201 | Estado: PASSED
- **CP-PROD-11:** Crear producto con precio igual a 0 | RN04 | Esperado: HTTP 422 | Estado: PASSED
- **CP-PROD-12:** Crear producto con precio negativo (-1000) | RN04 | Esperado: HTTP 422 | Estado: PASSED
- **CP-PROD-13:** Crear producto con precio mínimo positivo (0.01) | RN04 | Esperado: HTTP 201 | Estado: PASSED
- **CP-PROD-14:** Crear producto con stock igual a 0 | RN05/RN07 | Esperado: HTTP 201 | Estado: PASSED
- **CP-PROD-15:** Crear producto con stock negativo (-1) | RN05 | Esperado: HTTP 422 | Estado: PASSED
- **CP-PROD-16:** Crear producto con categoría inexistente | RN06 | Esperado: HTTP 404 | Estado: PASSED
- **CP-PROD-17:** Precio inválido al actualizar | RN08 | Esperado: HTTP 422 | Estado: PASSED
- **CP-PROD-18:** Categoría inexistente al actualizar | RN08/RN06 | Esperado: HTTP 404 | Estado: PASSED
