# Pruebas Automatizadas - Patio de Juegos

## 📋 Descripción General

Proyecto de automatización de pruebas para la aplicación **Patio de Juegos** utilizando Selenium y Python. Implementa pruebas end-to-end para operaciones CRUD de productos, autenticación y carrito de compras.

## 🎯 Objetivo del Proyecto

Desarrollar un conjunto robusto de pruebas automatizadas que verifiquen:
- ✅ Autenticación (Login)
- ✅ Operaciones CRUD (Crear, Leer, Actualizar, Eliminar productos)
- ✅ Funcionalidad de carrito de compras
- ✅ Validación de datos y manejo de errores

## 📊 Cobertura de Pruebas

### Historias de Usuario: 6
- **HU-001**: Autenticación (Login)
- **HU-002**: Crear Producto
- **HU-003**: Listar Productos
- **HU-004**: Editar Producto
- **HU-005**: Eliminar Producto
- **HU-006**: Carrito de Compras

### Casos de Prueba: 23
Cada historia incluye:
- 1 caso de **Camino Feliz** (flujo principal exitoso)
- 1 caso de **Prueba Negativa** (manejo de errores)
- 1-2 casos de **Pruebas de Límites** (validación de bordes)

### Screenshots: Automáticos
Se captura pantalla en cada paso de prueba para documentación y debugging.

## 🛠️ Prerequisitos

### Software Requerido
- Python 3.7+
- pip (gestor de paquetes de Python)
- Un navegador web (Chrome recomendado)

### Instalación

```bash
# 1. Clonar o descargar el proyecto
cd /workspaces/Patio-de-juegos

# 2. Instalar dependencias
pip install -r requirements.txt

# 3. (Opcional) Verificar instalación
python -c "import selenium; import pytest; print('✓ Dependencias instaladas')"
```

## 🚀 Uso

### Preparación Inicial

1. **Inicia el servidor web** en la carpeta `docs/`:
```bash
cd docs
python3 -m http.server 8000
# El servidor estará disponible en: http://localhost:8000
```

2. **Abre otra terminal** para ejecutar las pruebas

### Ejecutar Todas las Pruebas

```bash
./run_tests.sh
```

O manualmente:

```bash
cd tests/automation
python3 -m pytest test_cases/ \
    -v \
    --html=../../reports/test_report.html \
    --self-contained-html
```

### Ejecutar Pruebas Específicas

```bash
# Solo pruebas de login
cd tests/automation
python3 -m pytest test_cases/test_login.py -v

# Solo pruebas CRUD (crear, listar, editar, eliminar)
python3 -m pytest test_cases/test_crear.py test_cases/test_lista.py test_cases/test_editar.py test_cases/test_eliminar.py -v

# Solo pruebas de carrito
python3 -m pytest test_cases/test_carrito.py -v
```

### Opciones Útiles

```bash
# Mostrar prints durante ejecución
python3 -m pytest test_cases/ -v -s

# Detener en primer error
python3 -m pytest test_cases/ -v -x

# Ejecutar solo pruebas que pasen/fallen anteriormente
python3 -m pytest test_cases/ --lf  # last failed
python3 -m pytest test_cases/ --ff  # failed first

# Ejecución en paralelo (más rápido)
python3 -m pytest test_cases/ -v -n auto

# Reporte detallado en JSON
python3 -m pytest test_cases/ --json=report.json
```

## 📁 Estructura del Proyecto

```
tests/automation/
├── conftest.py                 # Configuración y fixtures de pytest
├── config/
│   └── config.py              # Variables de configuración
├── pages/                      # Page Object Model
│   ├── base_page.py           # Clase base para todas las páginas
│   ├── index_page.py          # Página de login/registro
│   ├── crear_page.py          # Página de crear producto
│   ├── lista_page.py          # Página de listar productos
│   ├── editar_page.py         # Página de editar producto
│   └── carrito_page.py        # Página de carrito
├── test_cases/                # Suite de pruebas
│   ├── test_login.py          # Pruebas de autenticación
│   ├── test_crear.py          # Pruebas de crear producto
│   ├── test_lista.py          # Pruebas de listar productos
│   ├── test_editar.py         # Pruebas de editar producto
│   ├── test_eliminar.py       # Pruebas de eliminar producto
│   └── test_carrito.py        # Pruebas de carrito
└── utils/
    └── helpers.py             # Funciones de utilidad

reports/
├── test_report.html           # Reporte HTML principal
├── screenshots/               # Capturas de pantalla automáticas
└── pytest.log                 # Log de ejecución

docs/                          # Aplicación web (frontend)
├── HTML/                      # Páginas HTML
│   ├── Index.html
│   ├── Crear.html
│   ├── Lista.html
│   ├── Editar.html
│   └── Carrito.html
├── JS/                        # Lógica JavaScript
└── CSS/                       # Estilos
```

## 🔧 Configuración

Editar `tests/automation/config/config.py`:

```python
# URLs
BASE_URL = "http://localhost:8000/HTML"

# Credenciales
ADMIN_USER = "admin"
ADMIN_PASSWORD = "123"
TEST_USER = "test_user"
TEST_PASSWORD = "password123"

# Navegador
BROWSER = "chrome"  # Options: chrome, firefox, edge
HEADLESS = False    # True para modo sin interfaz

# Timeouts
WAIT_TIMEOUT = 15   # Segundos para esperar elementos
```

## 📊 Reportes

### HTML Report
Después de ejecutar las pruebas, abre:
```
reports/test_report.html
```

El reporte contiene:
- ✅ Resumen de pruebas (pasadas, fallidas, omitidas)
- ✅ Detalle de cada prueba
- ✅ Screenshots automáticos
- ✅ Logs de ejecución
- ✅ Duraciones

### Screenshots
Todas las capturas se guardan en:
```
reports/screenshots/
```

## 🧪 Tipos de Prueba

### 1. Camino Feliz (Happy Path)
- Verifica el flujo principal exitoso
- Utiliza datos válidos
- Espera resultados positivos

### 2. Pruebas Negativas
- Verifica manejo de errores
- Utiliza datos inválidos
- Espera mensajes de error apropiados

### 3. Pruebas de Límites
- Verifica límites de campos
- Caracteres especiales
- Valores extremos (muy largos, negativos, etc.)

## 🔑 Credenciales de Prueba

### Admin (para crear/editar/eliminar productos)
```
Usuario: admin
Contraseña: 123
```

### Usuario Regular (para compras)
```
Usuario: test_user
Contraseña: password123
```

Nota: Los usuarios de prueba se pueden crear/registrar en la aplicación.

## 🐛 Troubleshooting

### Problema: "ConnectionRefusedError: [Errno 111] Connection refused"
**Solución**: El servidor web no está corriendo
```bash
cd docs
python3 -m http.server 8000
```

### Problema: "selenium.common.exceptions.TimeoutException"
**Solución**: El elemento no se encontró en el tiempo especificado
- Verificar que los localizadores (By.ID, By.XPATH) sean correctos
- Aumentar WAIT_TIMEOUT en config.py
- Verificar que los elementos existan en el HTML

### Problema: "No module named 'selenium'"
**Solución**: Reinstalar dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Problema: "Chrome driver version mismatch"
**Solución**: webdriver-manager descarga automáticamente el driver correcto
```bash
# Limpiar cache de drivers
rm -rf ~/.wdm/
```

## 📝 Agregar Nuevas Pruebas

1. **Crear archivo de prueba** en `test_cases/`:
```python
# test_cases/test_nueva_feature.py
import pytest
from pages.nueva_page import NuevaPage

class TestNuevaFeature:
    @pytest.fixture(autouse=True)
    def setup(self, driver):
        self.page = NuevaPage(driver)
        self.page.navigate_to()
    
    def test_algo(self):
        # Tu prueba aquí
        pass
```

2. **Crear Page Object** en `pages/`:
```python
# pages/nueva_page.py
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class NuevaPage(BasePage):
    # Localizadores
    ELEMENTO = (By.ID, "elemento_id")
    
    def __init__(self, driver):
        super().__init__(driver, url)
    
    def alguna_accion(self):
        # Acción aquí
        pass
```

## 📚 Documentación Adicional

- **USER_STORIES.md**: Detalle de todas las historias de usuario
- **requirements.txt**: Dependencias del proyecto
- **pytest.ini**: Configuración de pytest

## 🔗 Migración a Jira/Azure DevOps

Las historias de usuario están documentadas en `USER_STORIES.md`. Para migrar:

1. Crear un proyecto en Jira o Azure DevOps
2. Copiar cada HU-XXX como un Issue de tipo "Story"
3. Copiar cada HU-XXX-TC-YYY como un Issue de tipo "Test Case"
4. Enlazar Test Cases con sus Stories correspondientes
5. Usar los archivos Python como documentación técnica

## 📊 Métricas

**Estado Actual**:
- ✅ 6 Historias de Usuario
- ✅ 23+ Casos de Prueba
- ✅ 3 Tipos de Prueba (Camino Feliz, Negativa, Límites)
- ✅ Screenshots Automáticos
- ✅ Reportes HTML
- ✅ Page Object Model
- ✅ Locales: Español

## 🔐 Notas de Seguridad

- ⚠️ Las credenciales en config.py son solo para testing
- ⚠️ Nunca usar en producción
- ⚠️ No compartir credenciales reales en el repositorio
- ⚠️ Usar variables de entorno para datos sensibles en CI/CD

## 📝 Licencia

Este proyecto es parte de la tarea de automatización de pruebas.

## 👨‍💻 Soporte

Para preguntas o problemas:
1. Revisar USER_STORIES.md
2. Verificar logs en reports/pytest.log
3. Revisar screenshots en reports/screenshots/
4. Consultar documentación de Selenium en https://selenium.dev/

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0  
**Estado**: ✅ Funcional
