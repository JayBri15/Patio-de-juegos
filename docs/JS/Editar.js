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
  // DEBUG: registrar producto cargado
  try { console.debug('[Editar.js] loadProductToForm - loaded product', p); } catch (e) {}
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
  try { console.debug('[Editar.js] form element present?', !!form); } catch (e) {}
  try { console.debug('[Editar.js] ready to attach submit listener'); } catch (e) {}
  form.addEventListener('submit', (e) => {
    e.preventDefault();
    const id = document.getElementById('editId').value;
    const name = document.getElementById('editName').value.trim();
    const desc = document.getElementById('editDesc').value.trim();
    const price = parseFloat(document.getElementById('editPrice').value);
    const stock = parseInt(document.getElementById('editStock').value, 10);
    // DEBUG: entrada al handler de submit
    try { console.debug('[Editar.js] submit handler start', { id, name, desc, price, stock }); } catch (e) {}
    if (!name || isNaN(price) || isNaN(stock)) { showMessage('Completa todos los campos correctamente.', 'error'); return; }

    // read products once, find index and update in-place to avoid inconsistent reads
    const editImageInput = document.getElementById('editImage');
    const items = getProducts();
    const idx = items.findIndex(u => u.id === id);
    if (idx === -1) { showMessage('Producto no encontrado.', 'error'); return; }

    const existing = items[idx] || {};
    const updated = { ...existing, name, desc, price, stock };

    // If a new image was selected, read it asynchronously and save when ready
    if (editImageInput && editImageInput.files && editImageInput.files[0]) {
      const f = editImageInput.files[0];
      try { console.debug('[Editar.js] new image selected', { name: f.name, type: f.type, size: f.size }); } catch (e) {}
      if (!f.type || !f.type.startsWith('image/')) { showMessage('El archivo seleccionado no es una imagen válida.', 'error'); editImageInput.value = ''; return; }
      if (f.size > IMAGE_MAX_BYTES) { showMessage('La imagen es demasiado grande. Máx 200 KB.', 'error'); editImageInput.value = ''; return; }
      const fr = new FileReader();
      fr.onload = () => {
        try { console.debug('[Editar.js] FileReader.onload - result length', fr.result && fr.result.length); } catch (e) {}
        updated.image = fr.result;
        try { console.debug('[Editar.js] about to write updated item', { idx, updated }); } catch (e) {}
        items[idx] = updated;
        saveProducts(items);
        try { console.debug('[Editar.js] saved products, new length', items.length); } catch (e) {}
        window.location.href = 'Lista.html';
      };
      fr.readAsDataURL(f);
      return;
    }

    // no new image: preserve existing image value
    updated.image = existing.image || null;
    try { console.debug('[Editar.js] about to write updated item (no new image)', { idx, updated }); } catch (e) {}
    items[idx] = updated;
    saveProducts(items);
    try { console.debug('[Editar.js] saved products (no new image), new length', items.length); } catch (e) {}
    window.location.href = 'Lista.html';
  });
  try { console.debug('[Editar.js] submit listener attached'); } catch (e) {}
  // additionally log clicks on the submit button to detect whether clicks reach the button
  try {
    const submitBtn = form.querySelector("button[type='submit']");
    if (submitBtn) {
      submitBtn.addEventListener('click', () => { try { console.debug('[Editar.js] submit button clicked'); } catch(e){} });
    } else {
      try { console.debug('[Editar.js] submit button not found'); } catch(e){}
    }
  } catch (e) { console.error(e); }

  // capture global errors to ensure no silent exceptions stop handlers
  window.addEventListener('error', function(ev) { try { console.error('[Editar.js] window.onerror', ev && ev.error ? ev.error.stack || ev.error : ev); } catch(e){} });

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

