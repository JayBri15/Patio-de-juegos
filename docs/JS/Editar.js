/*
 * Editar.js — Página de edición de producto.
 * Responsable de: cargar un producto por `id` (query param), mostrar datos en el formulario,
 * permitir reemplazar/preview de imagen, auto-ajustar textarea de descripción y guardar cambios
 * en `pdj_products_v1` (preservando imagen si no se reemplaza).
 */

// Página de edición: carga producto por id (query param) y permite guardar cambios
const STORAGE_KEY = 'pdj_products_v1';
// max image size in bytes (200 KB)
const IMAGE_MAX_BYTES = 200 * 1024;

function getProducts() {
  try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) : []; }
  catch (e) { console.error(e); return []; }
}

function saveProducts(items) { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); }

function qs(param) {
  const url = new URL(window.location.href);
  return url.searchParams.get(param);
}

function loadProductToForm(id) {
  const items = getProducts();
  const p = items.find(x => x.id === id);
  if (!p) {
    showMessage('Producto no encontrado.', 'error');
    setTimeout(() => { window.location.href = 'Crear.html'; }, 1500);
    return null;
  }
  document.getElementById('editId').value = p.id;
  document.getElementById('editName').value = p.name || '';
  document.getElementById('editDesc').value = p.desc || '';
  document.getElementById('editPrice').value = p.price || '';
  document.getElementById('editStock').value = p.stock || '';
  // image preview
  const preview = document.getElementById('editPreview');
  if (p.image) { preview.src = p.image; preview.style.display = 'block'; } else { preview.src = ''; preview.style.display = 'none'; }
  return p;
}

// auto-resize helper for textareas
function autoResizeTextarea(el) {
  if (!el) return;
  el.style.height = 'auto';
  el.style.height = (el.scrollHeight) + 'px';
}

document.addEventListener('DOMContentLoaded', () => {
  const id = qs('id');
  if (!id) { showMessage('Falta id de producto.', 'error'); setTimeout(() => { window.location.href = 'Crear.html'; }, 1500); return; }
  loadProductToForm(id);

  const form = document.getElementById('editForm');
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const id = document.getElementById('editId').value;
    const name = document.getElementById('editName').value.trim();
    const desc = document.getElementById('editDesc').value.trim();
    const price = parseFloat(document.getElementById('editPrice').value);
    const stock = parseInt(document.getElementById('editStock').value, 10);
    if (!name || isNaN(price) || isNaN(stock)) { showMessage('Completa todos los campos correctamente.', 'error'); return; }
    // handle optional new image
    const editImageInput = document.getElementById('editImage');
    const items = getProducts().map(u => u.id === id ? { ...u, name, desc, price, stock } : u);
    const target = items.find(x => x.id === id);
    const existing = getProducts().find(x => x.id === id) || {};
    if (editImageInput && editImageInput.files && editImageInput.files[0]) {
      const f = editImageInput.files[0];
      if (!f.type || !f.type.startsWith('image/')) { showMessage('El archivo seleccionado no es una imagen válida.', 'error'); editImageInput.value = ''; return; }
      if (f.size > IMAGE_MAX_BYTES) { showMessage('La imagen es demasiado grande. Máx 200 KB.', 'error'); editImageInput.value = ''; return; }
      // read file sync via FileReader promise
      const fr = new FileReader();
      fr.onload = () => {
        target.image = fr.result;
        saveProducts(items);
        // after saving edits, go to product list
        window.location.href = 'Lista.html';
      };
      fr.readAsDataURL(f);
      return;
    } else {
      // keep existing image
      target.image = existing.image || null;
    }
    saveProducts(items);
    // after saving edits, go to product list
    window.location.href = 'Lista.html';
  });

  // preview when selecting new image
  const editImageInputEl = document.getElementById('editImage');
  const editPreviewEl = document.getElementById('editPreview');
  if (editImageInputEl) {
    editImageInputEl.addEventListener('change', () => {
      const f = editImageInputEl.files && editImageInputEl.files[0];
      if (!f) { if (editPreviewEl) { editPreviewEl.style.display = 'none'; editPreviewEl.src = ''; } return; }
      // validate type and size
      if (!f.type || !f.type.startsWith('image/')) {
        showMessage('El archivo seleccionado no es una imagen válida.', 'error');
        editImageInputEl.value = '';
        if (editPreviewEl) { editPreviewEl.style.display = 'none'; editPreviewEl.src = ''; }
        return;
      }
      if (f.size > IMAGE_MAX_BYTES) {
        showMessage('La imagen es demasiado grande. Máx 200 KB.', 'error');
        editImageInputEl.value = '';
        if (editPreviewEl) { editPreviewEl.style.display = 'none'; editPreviewEl.src = ''; }
        return;
      }
      const fr = new FileReader();
      fr.onload = () => { if (editPreviewEl) { editPreviewEl.src = fr.result; editPreviewEl.style.display = 'block'; } };
      fr.readAsDataURL(f);
    });
  }

  // wire choose image button
  const chooseEditImageBtn = document.getElementById('chooseEditImageBtn');
  if (chooseEditImageBtn && editImageInputEl) {
    chooseEditImageBtn.addEventListener('click', () => editImageInputEl.click());
  }

  const cancel = document.getElementById('cancelEdit');
  cancel.addEventListener('click', () => { window.location.href = 'Lista.html'; });
  const gotoBtn = document.getElementById('gotoCrear');
  if (gotoBtn) gotoBtn.addEventListener('click', () => { window.location.href = 'Crear.html'; });

  // auto-resize for description textarea
  const editDesc = document.getElementById('editDesc');
  if (editDesc) {
    setTimeout(() => autoResizeTextarea(editDesc), 50);
    editDesc.addEventListener('input', () => autoResizeTextarea(editDesc));
  }
});

