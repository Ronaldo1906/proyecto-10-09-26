# Matriz de Trazabilidad
| ID Requisito | Descripción | Casos de Prueba Relacionados | Estado Cobertura |
|---|---|---|---|
| **RF01 / RN01** | Crear categoría válida (3-60 chars) | CP-CAT-01, CP-CAT-05, CP-CAT-06 | Cubierto |
| **RF02 / RN02** | Listar categorías / Nombre único (case-insensitive) | CP-CAT-02, CP-CAT-07 | Cubierto |
| **RF03 / RF04** | Consultar categoría por ID / Rechazar inexistente | CP-CAT-03, CP-CAT-04 | Cubierto |
| **RF05 / RN03** | Crear producto válido (Nombre 3-80 chars) | CP-PROD-01, CP-PROD-09, CP-PROD-10 | Cubierto |
| **RF06 / RF07** | Listar productos / Consultar producto por ID | CP-PROD-02, CP-PROD-03 | Cubierto |
| **RF08** | Responder 404 al consultar producto inexistente | CP-PROD-04 | Cubierto |
| **RF09 / RF10** | Actualizar producto existente / Responder 404 | CP-PROD-05, CP-PROD-06 | Cubierto |
| **RF11 / RF12** | Eliminar producto existente / Responder 404 | CP-PROD-07, CP-PROD-08 | Cubierto |
| **RN04** | Precio de producto estrictamente > 0 | CP-PROD-11, CP-PROD-12, CP-PROD-13 | Cubierto |
| **RN05 / RN07** | Stock >= 0 (Permitir stock = 0) | CP-PROD-14, CP-PROD-15 | Cubierto |
| **RN06 / RN08** | Categoría asignada debe existir / Mantener validaciones | CP-PROD-16, CP-PROD-17, CP-PROD-18 | Cubierto |
