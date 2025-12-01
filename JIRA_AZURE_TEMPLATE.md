# Historias de Usuario - Importación a Jira/Azure DevOps

Esta documentación facilita la creación de historias y casos de prueba en herramientas de gestión de proyectos.

## 📋 Proceso de Importación

### Opción 1: Jira Cloud

1. Ve a tu proyecto en Jira
2. Clic en "Crear" (Create)
3. Para cada historia, completa:
   - **Tipo**: Story
   - **Resumen**: HU-001: Autenticación (Login)
   - **Descripción**: (copiar de abajo)
   - **Criterios de Aceptación**: (copiar)

4. Después de crear la Story, crea Test Cases vinculados

### Opción 2: Azure DevOps

1. Ve a "Work Items"
2. "New Work Item" → "User Story"
3. Completa los campos
4. Agrega "Test Cases" desde la pestaña "Child Links"

### Opción 3: Importación via CSV/JSON (Avanzado)

Usar herramientas como jira-python o rest-apis para importación automatizada.

---

## HU-001: Autenticación

```
Tipo: Story
ID: HU-001
Título: Como usuario, deseo poder iniciar sesión para acceder a mis funcionalidades

Descripción:
- El usuario debe poder iniciar sesión con sus credenciales
- Las credenciales se validan contra el sistema de usuarios
- La sesión se mantiene durante la navegación
- El usuario puede cerrar sesión cuando sea necesario

Criterios de Aceptación:
[ ] Login exitoso con credenciales válidas (admin/123)
[ ] Redirección correcta a página de productos
[ ] Sesión guardada en sessionStorage
[ ] Mensaje de error con credenciales inválidas
[ ] Validación de campos no vacíos

Criterios de Rechazo:
[ ] No permitir login sin usuario o contraseña
[ ] No redirigir con credenciales incorrectas
[ ] No guardar sesión de usuario inválido

Archivos Técnicos:
- Código: tests/automation/test_cases/test_login.py
- Page Object: tests/automation/pages/index_page.py
```

### Test Cases para HU-001

```
TC-001: Login Exitoso
Tipo: Test Case
Vinculado a: HU-001

Precondición: Usuario en página de login
Pasos:
1. Ingresa usuario: "admin"
2. Ingresa contraseña: "123"
3. Hace clic en "Acceder"

Resultado esperado: Redirecciona a Lista.html

----

TC-002: Login Fallido
Tipo: Test Case
Vinculado a: HU-001

Precondición: Usuario en página de login
Pasos:
1. Ingresa usuario: "invalid"
2. Ingresa contraseña: "wrong"
3. Hace clic en "Acceder"

Resultado esperado: Muestra error, permanece en Index.html

----

TC-003: Campos Vacíos
Tipo: Test Case
Vinculado a: HU-001

Precondición: Usuario en página de login
Pasos:
1. Deja campos vacíos
2. Hace clic en "Acceder"

Resultado esperado: Muestra validación, permanece en Index.html

----

TC-004: Contraseña Muy Larga
Tipo: Test Case
Vinculado a: HU-001

Precondición: Usuario en página de login
Pasos:
1. Ingresa usuario: "admin"
2. Ingresa contraseña de 200+ caracteres
3. Hace clic en "Acceder"

Resultado esperado: Valida límites, muestra error
```

---

## HU-002: Crear Producto

```
Tipo: Story
ID: HU-002
Título: Como administrador, deseo crear nuevos productos para el catálogo

Descripción:
- Solo administradores pueden acceder al formulario de creación
- Se pueden ingresar todos los detalles del producto
- Se valida que los datos sean correctos
- El producto se guarda y aparece en la lista

Criterios de Aceptación:
[ ] Acceso restringido solo para admin
[ ] Formulario con campos: nombre, precio, descripción, categoría
[ ] Validación de campos requeridos
[ ] Validación de precio (números positivos)
[ ] Redirección a lista después de guardar
[ ] Producto visible en la lista

Criterios de Rechazo:
[ ] No permitir crear sin nombre o precio
[ ] No permitir precio negativo o cero
[ ] No guardar sin validación exitosa

Archivos Técnicos:
- Código: tests/automation/test_cases/test_crear.py
- Page Object: tests/automation/pages/crear_page.py
```

### Test Cases para HU-002

```
TC-001: Crear Producto Válido
TC-002: Campos Requeridos Faltantes
TC-003: Caracteres Especiales
TC-004: Precio Negativo
```

---

## HU-003: Listar Productos

```
Tipo: Story
ID: HU-003
Título: Como usuario, deseo ver lista de productos disponibles

Descripción:
- Se muestra tabla con todos los productos
- Cada producto muestra: nombre, precio, descripción
- Hay opciones de editar, eliminar (admin), agregar al carrito
- Se puede buscar productos
- Manejo de lista vacía

Criterios de Aceptación:
[ ] Tabla cargada correctamente
[ ] Todos los campos del producto visible
[ ] Botones funcionales (editar, eliminar, carrito)
[ ] Búsqueda filtra productos
[ ] Mensaje cuando no hay productos

Criterios de Rechazo:
[ ] No mostrar productos eliminados
[ ] No mostrar datos incorrectos o incompletos

Archivos Técnicos:
- Código: tests/automation/test_cases/test_lista.py
- Page Object: tests/automation/pages/lista_page.py
```

### Test Cases para HU-003

```
TC-001: Ver Lista de Productos
TC-002: Lista Vacía
TC-003: Búsqueda de Productos
TC-004: Búsqueda con Caracteres Especiales
```

---

## HU-004: Editar Producto

```
Tipo: Story
ID: HU-004
Título: Como administrador, deseo editar productos existentes

Descripción:
- Solo admin puede editar
- Se cargan datos actuales del producto
- Se pueden modificar todos los campos
- Se valida información
- Cambios se guardan en la base de datos

Criterios de Aceptación:
[ ] Acceso restringido a admin
[ ] Datos actuales se cargan correctamente
[ ] Se pueden modificar: nombre, precio, descripción, categoría
[ ] Validación de campos requeridos
[ ] Cambios se persisten
[ ] Redirección exitosa a lista

Criterios de Rechazo:
[ ] No permitir campos vacíos requeridos
[ ] No permitir precio negativo

Archivos Técnicos:
- Código: tests/automation/test_cases/test_editar.py
- Page Object: tests/automation/pages/editar_page.py
```

### Test Cases para HU-004

```
TC-001: Editar con Datos Válidos
TC-002: Datos Inválidos (precio no numérico)
TC-003: Campo Requerido Vacío
TC-004: Descripción Muy Larga
```

---

## HU-005: Eliminar Producto

```
Tipo: Story
ID: HU-005
Título: Como administrador, deseo eliminar productos

Descripción:
- Solo admin puede eliminar
- Confirmación antes de eliminar
- Producto se remueve del catálogo
- Se puede cancelar la operación

Criterios de Aceptación:
[ ] Botón eliminar visible (solo admin)
[ ] Diálogo de confirmación
[ ] Producto se remueve completamente
[ ] Se puede cancelar
[ ] Mensaje de confirmación

Criterios de Rechazo:
[ ] No eliminar sin confirmación
[ ] No permitir acceso a producto eliminado

Archivos Técnicos:
- Código: tests/automation/test_cases/test_eliminar.py
```

### Test Cases para HU-005

```
TC-001: Eliminar Exitosamente
TC-002: Cancelar Eliminación
TC-003: Eliminar Múltiples Productos
```

---

## HU-006: Carrito de Compras

```
Tipo: Story
ID: HU-006
Título: Como usuario, deseo usar carrito para organizar mis compras

Descripción:
- Agregar productos al carrito
- Ver detalle de carrito
- Remover productos
- Actualizar cantidades
- Persistencia durante la sesión

Criterios de Aceptación:
[ ] Agregar producto al carrito funciona
[ ] Carrito muestra productos agregados
[ ] Se puede remover productos
[ ] Cantidad se puede actualizar
[ ] Carrito persiste durante sesión

Criterios de Rechazo:
[ ] No permitir cantidad negativa
[ ] No perder carrito sin confirmación

Archivos Técnicos:
- Código: tests/automation/test_cases/test_carrito.py
- Page Object: tests/automation/pages/carrito_page.py
```

### Test Cases para HU-006

```
TC-001: Agregar al Carrito
TC-002: Carrito Vacío
TC-003: Múltiples Productos
TC-004: Remover del Carrito
```

---

## 📊 Matriz de Cobertura

| Categoría | HU-001 | HU-002 | HU-003 | HU-004 | HU-005 | HU-006 |
|-----------|:------:|:------:|:------:|:------:|:------:|:------:|
| Camino Feliz | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Negativa | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| Límites | ✅✅ | ✅✅ | ✅✅ | ✅✅ | ✅ | ✅✅ |
| **Total** | **4** | **4** | **4** | **4** | **3** | **4** |

---

## 🔗 Vinculación de Historias a Casos de Prueba

Para vincular en Jira/Azure DevOps:

1. **En Jira**:
   - Abrir la Story
   - "Link" → "Links" → "Vincula un caso de prueba"
   - Seleccionar el Test Case

2. **En Azure DevOps**:
   - Abrir el User Story
   - Pestaña "Child Links"
   - "Link to a new test case"
   - Crear o seleccionar caso de prueba

---

## 📝 Notas Adicionales

### Etiquetas Sugeridas (Tags)
- `automation` - Prueba automatizada
- `selenium` - Usa Selenium
- `crud` - Operación CRUD
- `authentication` - Autenticación
- `e2e` - End-to-end

### Sprints Sugeridos
- Sprint 1: HU-001 (Login) + HU-002 (Crear)
- Sprint 2: HU-003 (Listar) + HU-004 (Editar)
- Sprint 3: HU-005 (Eliminar) + HU-006 (Carrito)

### Estimación
- HU-001 a HU-006: 8 puntos cada una (40 horas de trabajo)
- Pruebas: 21 puntos (40 horas)
- Documentación: 5 puntos (8 horas)
- **Total**: 34 puntos (~128 horas)

---

**Generado**: Diciembre 2024  
**Versión**: 1.0
