# Historias de Usuario - Patio de Juegos

Documentación de historias de usuario para el proyecto de automatización con Selenium.

## HU-001: Autenticación (Login)

### Descripción
Como usuario, deseo poder iniciar sesión en la aplicación para acceder a mis funcionalidades personalizadas.

### Criterios de Aceptación
- ✓ El usuario puede iniciar sesión con credenciales válidas (admin/123)
- ✓ Se redirige correctamente a la página de lista de productos
- ✓ Se guarda la sesión en sessionStorage
- ✓ Se muestra mensaje de error con credenciales inválidas
- ✓ Se valida que los campos no estén vacíos

### Criterios de Rechazo
- ✗ No se debe permitir login sin usuario o contraseña
- ✗ No se debe redirigir con credenciales incorrectas
- ✗ No se debe guardar sesión de usuario inválido

### Casos de Prueba
- **HU-001-TC-001** (Camino Feliz): Login exitoso con credenciales válidas
- **HU-001-TC-002** (Negativa): Login fallido con credenciales inválidas
- **HU-001-TC-003** (Límites): Login con campos vacíos
- **HU-001-TC-004** (Límites): Login con contraseña muy larga (200+ caracteres)

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_login.py`
- Page Object: `tests/automation/pages/index_page.py`

---

## HU-002: Crear Producto

### Descripción
Como administrador, deseo poder crear nuevos productos para agregar al catálogo de la tienda.

### Criterios de Aceptación
- ✓ El admin puede acceder al formulario de creación de productos
- ✓ Se puede ingresar nombre, precio, descripción y categoría
- ✓ Se valida que los campos requeridos no estén vacíos
- ✓ Se acepta el producto y se redirige a la lista
- ✓ El producto aparece en la lista de productos

### Criterios de Rechazo
- ✗ No se debe permitir crear producto sin nombre o precio
- ✗ No se debe permitir precio negativo
- ✗ No se debe redirigir sin guardar el producto

### Casos de Prueba
- **HU-002-TC-001** (Camino Feliz): Crear producto con datos válidos
- **HU-002-TC-002** (Negativa): Crear producto sin campos requeridos
- **HU-002-TC-003** (Límites): Crear producto con caracteres especiales
- **HU-002-TC-004** (Límites): Crear producto con precio negativo

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_crear.py`
- Page Object: `tests/automation/pages/crear_page.py`

---

## HU-003: Listar Productos

### Descripción
Como usuario, deseo ver la lista de productos disponibles para poder seleccionar y comprar.

### Criterios de Aceptación
- ✓ La lista de productos se muestra correctamente
- ✓ Se muestran todos los campos: nombre, precio, descripción
- ✓ Se pueden ver opciones para editar, eliminar o agregar al carrito
- ✓ La búsqueda de productos funciona correctamente
- ✓ Se muestra mensaje cuando no hay productos

### Criterios de Rechazo
- ✗ No se deben mostrar productos eliminados
- ✗ No se debe permitir búsqueda sin validación
- ✗ No se deben mostrar precios negativos o inválidos

### Casos de Prueba
- **HU-003-TC-001** (Camino Feliz): Ver lista de productos
- **HU-003-TC-002** (Negativa): Lista vacía sin productos
- **HU-003-TC-003** (Límites): Búsqueda de productos
- **HU-003-TC-004** (Límites): Búsqueda con caracteres especiales

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_lista.py`
- Page Object: `tests/automation/pages/lista_page.py`

---

## HU-004: Editar Producto

### Descripción
Como administrador, deseo poder editar los productos existentes para actualizar su información.

### Criterios de Aceptación
- ✓ El admin puede acceder a la página de edición de producto
- ✓ Se carga la información actual del producto
- ✓ Se pueden modificar todos los campos (nombre, precio, descripción, categoría)
- ✓ Se valida que los campos requeridos no estén vacíos
- ✓ Los cambios se guardan y se redirige a la lista

### Criterios de Rechazo
- ✗ No se debe permitir editar sin cambios válidos
- ✗ No se debe permitir dejar vacío un campo requerido
- ✗ No se debe permitir precio negativo

### Casos de Prueba
- **HU-004-TC-001** (Camino Feliz): Editar producto con datos válidos
- **HU-004-TC-002** (Negativa): Editar producto con datos inválidos
- **HU-004-TC-003** (Límites): Editar producto limpiando campos requeridos
- **HU-004-TC-004** (Límites): Editar producto con descripción muy larga

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_editar.py`
- Page Object: `tests/automation/pages/editar_page.py`

---

## HU-005: Eliminar Producto

### Descripción
Como administrador, deseo poder eliminar productos del catálogo cuando sea necesario.

### Criterios de Aceptación
- ✓ El admin puede hacer clic en botón eliminar
- ✓ Se solicita confirmación antes de eliminar
- ✓ El producto se elimina completamente del sistema
- ✓ Se puede cancelar la eliminación
- ✓ Se muestra mensaje de confirmación

### Criterios de Rechazo
- ✗ No se debe eliminar sin confirmación
- ✗ No se debe mostrar producto eliminado en la lista
- ✗ No se debe permitir acceder a producto eliminado

### Casos de Prueba
- **HU-005-TC-001** (Camino Feliz): Eliminar producto exitosamente
- **HU-005-TC-002** (Negativa): Cancelar eliminación de producto
- **HU-005-TC-003** (Límites): Eliminar múltiples productos

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_eliminar.py`

---

## HU-006: Carrito de Compras

### Descripción
Como usuario, deseo poder agregar productos al carrito para realizar compras.

### Criterios de Aceptación
- ✓ El usuario puede agregar productos al carrito
- ✓ Se muestra cantidad de items en el carrito
- ✓ Se puede ver detalle de productos en el carrito
- ✓ Se pueden remover productos del carrito
- ✓ El carrito persiste durante la sesión

### Criterios de Rechazo
- ✗ No se debe agregar producto con cantidad negativa
- ✗ No se debe perder carrito sin confirmación
- ✗ No se deben mostrar productos eliminados en carrito

### Casos de Prueba
- **HU-006-TC-001** (Camino Feliz): Agregar producto al carrito
- **HU-006-TC-002** (Negativa): Carrito vacío sin productos
- **HU-006-TC-003** (Límites): Agregar múltiples productos al carrito
- **HU-006-TC-004** (Límites): Remover producto del carrito

### Archivos Relacionados
- Casos de prueba: `tests/automation/test_cases/test_carrito.py`
- Page Object: `tests/automation/pages/carrito_page.py`

---

## Resumen de Cobertura

### Total de Historias: 6
### Total de Casos de Prueba: 24

| Historia | Camino Feliz | Negativa | Límites | Total |
|----------|:------------:|:--------:|:-------:|:-----:|
| HU-001 (Login) | 1 | 1 | 2 | 4 |
| HU-002 (Crear) | 1 | 1 | 2 | 4 |
| HU-003 (Listar) | 1 | 1 | 2 | 4 |
| HU-004 (Editar) | 1 | 1 | 2 | 4 |
| HU-005 (Eliminar) | 1 | 1 | 1 | 3 |
| HU-006 (Carrito) | 1 | 1 | 2 | 4 |
| **TOTAL** | **6** | **6** | **11** | **23** |

---

## Notas Técnicas

- **Framework**: Python con Selenium 4
- **Herramienta de Pruebas**: pytest
- **Page Object Model**: Implementado en `tests/automation/pages/`
- **Reportes**: HTML generado con pytest-html
- **Screenshots**: Automáticos en cada paso de prueba
- **Localización**: Español (español)

---

## Instrucciones para Migrar a Jira/Azure DevOps

1. Crear un proyecto o usar uno existente
2. Para cada historia (HU-XXX):
   - Crear un Issue de tipo "Story"
   - Copiar Descripción y Criterios de Aceptación/Rechazo
3. Para cada caso de prueba (HU-XXX-TC-YYY):
   - Crear un Issue de tipo "Test Case"
   - Enlazar con su History correspondiente
   - Incluir los pasos de ejecución

---

**Versión**: 1.0  
**Fecha**: Diciembre 2024  
**Autor**: Sistema de Automatización
