# Tarea-3-Uso-de-Git-y-Git-Flow

Breve guía y puntos importantes para probar la versión cliente del mini-proyecto.

Contenido principal
- `HTML/` — páginas estáticas: `Crear.html`, `Lista.html`, `Editar.html`, `Index.html`, `Carrito.html`.
- `JS/` — lógica cliente en JavaScript para cada página: `Crear.JS`, `Lista.js`, `Editar.js`, `Index.js`, `Carrito.js`, `ui.js` (utilidades de notificaciones).
- `CSS/` — estilos: `Crear.CSS`, `Lista.css`, `Editar.css`, `Carrito.css`, `Index.css`.

Arquitectura y almacenamiento
- Arquitectura: Frontend only — no hay servidor. Los datos se guardan en `localStorage` y `sessionStorage`.
- Llaves usadas:
  - Productos: `pdj_products_v1` (localStorage)
  - Usuarios: `crud_users_v1` (localStorage)
  - Sesión actual: `crud_current_user` (sessionStorage)
  - Carrito temporal: `pdj_cart` (sessionStorage)

Credenciales de administrador (demo)
- Usuario: `admin`
- Contraseña: `123`
- El admin puede acceder a `Crear.html` para crear/editar/eliminar productos.

Probar localmente
1. Abrir archivos directamente en el navegador:
  - Abre `docs/Tareas/tarea3_p3/HTML/Index.html`, registra o inicia sesión.
  - Como admin inicia sesión con `admin` / `123` y ve a `Crear.html`.

2. (Recomendado) Servidor simple (para evitar problemas con FileReader o rutas):
```bash
cd docs/Tareas/tarea3_p3
python3 -m http.server 8000
# luego en el navegador: http://localhost:8000/HTML/Index.html
```

Flujo de prueba rápido
- Registrar un usuario normal (registro guarda hashed password con SHA-256).
- Iniciar sesión como admin → `Crear.html` → crear un producto (puedes subir imagen pequeña).
- Ver `Lista.html` como usuario normal → agregar producto al carrito → `Carrito.html`.
- Editar un producto → `Editar.html?id=<id>`; al guardar redirige a la lista.

Notas y limitaciones
- Las imágenes se guardan como data URLs en `localStorage` (funciona sin servidor, pero puede consumir mucho espacio). Evita subir imágenes grandes.
- Los mensajes de error/éxito aparecen como notificaciones inline en la parte superior de cada página (reemplazo de `alert()`).

Posibles mejoras
- Reducción / compresión de imágenes antes de almacenar.
- Persistencia en servidor (APIs) para uso real.

