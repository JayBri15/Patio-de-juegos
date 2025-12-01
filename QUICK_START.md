# 🚀 GUÍA DE INICIO RÁPIDO - Pruebas Automatizadas

## ⚡ En 5 Minutos

### Paso 1: Verificar Instalación (1 min)
```bash
cd /workspaces/Patio-de-juegos
python3 validate_setup.py
```

Deberías ver ✓ en todas las validaciones (excepto el servidor web).

### Paso 2: Iniciar Servidor Web (en Terminal 1)
```bash
cd /workspaces/Patio-de-juegos/docs
python3 -m http.server 8000
```

Espera a ver:
```
Serving HTTP on 0.0.0.0 port 8000
```

### Paso 3: Ejecutar Pruebas (en Terminal 2)
```bash
cd /workspaces/Patio-de-juegos
./run_tests.sh
```

### Paso 4: Ver Resultados
Abre el reporte: `reports/test_report.html`

---

## 📊 Qué Esperar

### Salida de Ejecución
```
test_login.py::test_001_successful_login_with_valid_credentials PASSED
test_login.py::test_002_login_with_invalid_credentials PASSED
test_login.py::test_003_login_with_empty_fields PASSED
test_login.py::test_004_login_with_long_password PASSED

[... más pruebas ...]

======================== 23 passed in 245.32s ========================
```

### Archivos Generados
- `reports/test_report.html` - Reporte interactivo
- `reports/screenshots/` - ~100 imágenes automáticas
- `reports/pytest.log` - Log detallado

---

## 📝 Estructura de Pruebas

### 6 Historias de Usuario

#### HU-001: Login
- `test_001_successful_login_with_valid_credentials` ✅ Camino feliz
- `test_002_login_with_invalid_credentials` ❌ Negativa
- `test_003_login_with_empty_fields` ⚠️ Límites
- `test_004_login_with_long_password` ⚠️ Límites

#### HU-002: Crear Producto
- `test_001_create_product_with_valid_data` ✅ Camino feliz
- `test_002_create_product_with_missing_required_fields` ❌ Negativa
- `test_003_create_product_with_special_characters` ⚠️ Límites
- `test_004_create_product_with_negative_price` ⚠️ Límites

#### HU-003: Listar Productos
- `test_001_view_products_list` ✅ Camino feliz
- `test_002_empty_products_list` ❌ Negativa
- `test_003_search_products_functionality` ⚠️ Límites
- `test_004_search_with_special_characters` ⚠️ Límites

#### HU-004: Editar Producto
- `test_001_update_product_with_valid_data` ✅ Camino feliz
- `test_002_update_product_with_invalid_data` ❌ Negativa
- `test_003_update_product_with_empty_required_fields` ⚠️ Límites
- `test_004_update_product_with_long_description` ⚠️ Límites

#### HU-005: Eliminar Producto
- `test_001_delete_product_successfully` ✅ Camino feliz
- `test_002_cancel_product_deletion` ❌ Negativa
- `test_003_delete_multiple_products` ⚠️ Límites

#### HU-006: Carrito
- `test_001_add_product_to_cart` ✅ Camino feliz
- `test_002_empty_cart_scenario` ❌ Negativa
- `test_003_add_multiple_products_to_cart` ⚠️ Límites
- `test_004_remove_product_from_cart` ⚠️ Límites

---

## 🎯 Ejecutar Pruebas Específicas

### Solo Login
```bash
cd tests/automation
python3 -m pytest test_cases/test_login.py -v
```

### Solo CRUD
```bash
python3 -m pytest test_cases/test_crear.py test_cases/test_lista.py test_cases/test_editar.py test_cases/test_eliminar.py -v
```

### Solo Carrito
```bash
python3 -m pytest test_cases/test_carrito.py -v
```

### Una prueba específica
```bash
python3 -m pytest test_cases/test_login.py::TestLogin::test_001_successful_login_with_valid_credentials -v
```

### Con pantalla en terminal
```bash
python3 -m pytest test_cases/ -v -s
```

### Detener en primer error
```bash
python3 -m pytest test_cases/ -v -x
```

---

## 🔍 Entender los Resultados

### Reporte HTML
1. Abre `reports/test_report.html` en tu navegador
2. Verás:
   - **Summary**: Resumen de pruebas
   - **Tests**: Detalle de cada prueba
   - **Screenshots**: Imágenes de cada paso
   - **Logs**: Mensajes de debug

### Interpretar Resultados
```
✓ PASSED  → Prueba exitosa
✗ FAILED  → Prueba falló
⊗ SKIPPED → Prueba omitida
⚠ ERROR   → Error en la prueba
```

### Screenshots
- Guardadas automáticamente: `reports/screenshots/`
- Una por cada paso de la prueba
- Nombres descriptivos: `01_login_form_visible.png`

---

## 🛠️ Configuración

### Cambiar Navegador
Edita `tests/automation/config/config.py`:
```python
BROWSER = "chrome"  # Opciones: chrome, firefox, edge
HEADLESS = False    # True para ejecutar sin interfaz gráfica
```

### Cambiar Credenciales
```python
ADMIN_USER = "admin"
ADMIN_PASSWORD = "123"
TEST_USER = "test_user"
TEST_PASSWORD = "password123"
```

### Cambiar Timeouts
```python
WAIT_TIMEOUT = 15   # Segundos
EXPLICIT_WAIT = 10  # Segundos
```

---

## 🐛 Solucionar Problemas

### Error: "Connection refused"
```bash
# Terminal 1: Verifica que el servidor está corriendo
cd docs && python3 -m http.server 8000
```

### Error: "TimeoutException"
- Elemento no encontrado en 10 segundos
- Aumentar `WAIT_TIMEOUT` en config.py
- Verificar que el navegador está actualizado

### Error: "No module named 'selenium'"
```bash
pip install --upgrade -r requirements.txt
```

### Chrome driver desactualizado
```bash
# webdriver-manager lo actualiza automáticamente
# Si no funciona, limpiar cache:
rm -rf ~/.wdm/
```

### Las pruebas no avanzan
```bash
# Revisar los logs
cat reports/pytest.log | tail -50

# Ver qué sucede (sin headless)
# En config.py: HEADLESS = False
```

---

## 📚 Documentación

| Documento | Propósito |
|-----------|-----------|
| `EXECUTIVE_SUMMARY.md` | Resumen ejecutivo |
| `USER_STORIES.md` | Detalles de historias |
| `JIRA_AZURE_TEMPLATE.md` | Para migrar a Jira/Azure |
| `TESTING_README.md` | Guía completa |
| `validate_setup.py` | Validación del ambiente |

---

## ✅ Checklist Antes de Presentar

- [ ] Ejecuté `validate_setup.py` ✓
- [ ] Ejecuté `./run_tests.sh` ✓
- [ ] Revisé `reports/test_report.html` ✓
- [ ] Verifiqué screenshots en `reports/screenshots/` ✓
- [ ] Leí `USER_STORIES.md` ✓
- [ ] Revisé `EXECUTIVE_SUMMARY.md` ✓
- [ ] Las 6 historias están documentadas ✓
- [ ] 23+ casos de prueba funcionan ✓

---

## 🎬 Para la Presentación en Video

### Qué Mostrar
1. Estructura del proyecto (`tests/automation/`)
2. Ejecución de pruebas (`./run_tests.sh`)
3. Reporte HTML (`reports/test_report.html`)
4. Screenshots automáticas
5. Una prueba de camino feliz (éxito)
6. Una prueba negativa (error)
7. Código del Page Object Model
8. Historias de usuario documentadas

### Duración Sugerida
- Introducción: 2 min
- Demo de ejecución: 3 min
- Explicación de código: 5 min
- Resultados y reportes: 3 min
- Q&A: 2 min
- **Total**: 15 minutos

---

## 🎓 Aprendizajes Clave

### Conceptos Implementados
1. **Selenium**: Web scraping y automatización
2. **pytest**: Framework de testing
3. **Page Object Model**: Mantenibilidad del código
4. **Fixtures**: Reutilización de setup/teardown
5. **Screenshots**: Documentación automática
6. **Logging**: Trazabilidad de ejecución

### Mejores Prácticas
- ✓ Código limpio y legible
- ✓ Separación de concerns
- ✓ DRY (Don't Repeat Yourself)
- ✓ Documentación clara
- ✓ Manejo de errores robusto

---

## 📞 Soporte Rápido

### Validar Setup
```bash
python3 validate_setup.py
```

### Ver Logs Recientes
```bash
tail -50 reports/pytest.log
```

### Ejecutar en Debug
```bash
cd tests/automation
python3 -m pytest test_cases/ -v -s --tb=long
```

### Limpiar Reportes Anteriores
```bash
rm -rf reports/test_report.html reports/screenshots/*
```

---

**¡Listo para ejecutar!** 🚀

Cualquier pregunta: revisa los documentos en la carpeta raíz o consulta `TESTING_README.md`.

