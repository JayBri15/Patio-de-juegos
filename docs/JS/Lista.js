/*
 * Lista.js — Renderiza la lista pública de productos.
 * Responsable de: cargar productos desde localStorage (`pdj_products_v1`),
 * búsqueda/filtrado, mostrar miniaturas (o placeholder), mostrar acciones
 * según rol (editar/eliminar para admin, agregar al carrito para usuarios),
 * y manejo de UI de sesión (mostrar/ocultar botones de gestión).
 */

// Lista.js — renderiza la lista de productos, búsqueda, añadir al carrito
const STORAGE_KEY = 'pdj_products_v1';
const SESSION_KEY = 'crud_current_user';

// placeholder SVG used when no product image is available
const _SVG_PLACEHOLDER = `<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64'><rect width='100%' height='100%' fill='%23e6e9ef'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='%239ca3af' font-size='11'>No image</text></svg>`;
const PLACEHOLDER_IMG = 'data:image/svg+xml;utf8,' + encodeURIComponent(_SVG_PLACEHOLDER);

function getProducts() {
  try { const raw = localStorage.getItem(STORAGE_KEY); return raw ? JSON.parse(raw) : []; }
  catch (e) { console.error(e); return []; }
}
function saveProducts(items) { localStorage.setItem(STORAGE_KEY, JSON.stringify(items)); }

function getSession() {
  const raw = sessionStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : null;
}

function updateAuthUI() {
  const authActions = document.getElementById('authActions');
  const user = getSession();
  if (!authActions) return;
  if (user) {
    authActions.innerHTML = `
      <span class="muted">Bienvenido, ${user.name}</span>
      <button id="logoutBtn" class="btn" style="margin-left:8px">Cerrar Sesión</button>
    `;
    const btn = document.getElementById('logoutBtn');
    if (btn) btn.addEventListener('click', () => {
      sessionStorage.removeItem(SESSION_KEY);
      window.location.href = 'Index.html';
    });
  } else {
    authActions.innerHTML = '';
  }

  // show/hide manager button for admins only
  const parent = authActions.parentElement;
  let gotoBtn = document.getElementById('gotoManagerBtn');
  let gotoCartBtn = document.getElementById('gotoCartBtn');
  if (user && user.role === 'admin') {
    // ensure button exists
    if (!gotoBtn && parent) {
      gotoBtn = document.createElement('a');
      gotoBtn.id = 'gotoManagerBtn';
      gotoBtn.className = 'btn';
      gotoBtn.href = 'Crear.html';
      gotoBtn.textContent = 'Ir al Gestor de Productos';
      parent.insertBefore(gotoBtn, authActions);
    } else if (gotoBtn) {
      gotoBtn.style.display = '';
    }
    // hide cart button for admins
    if (gotoCartBtn) gotoCartBtn.style.display = 'none';
  } else {
    // hide manager button for non-admins
    if (gotoBtn) gotoBtn.remove();
    // show cart button for regular users
    if (gotoCartBtn) gotoCartBtn.style.display = '';
  }
}

function renderProducts(filter = '') {
  const items = getProducts();
    const q = document.getElementById('search').value.toLowerCase();
  const tbody = document.querySelector('#usersTable tbody');
  const emptyMessage = document.getElementById('emptyMessage');

  const filtered = items.filter(p => {
    if (!q) return true;
    return (p.name + ' ' + (p.desc || '')).toLowerCase().includes(q);
  });

  tbody.innerHTML = '';
  if (filtered.length === 0) {
    emptyMessage.style.display = 'block';
    return;
  }
  emptyMessage.style.display = 'none';

  const session = getSession();
  filtered.forEach(p => {
    const tr = document.createElement('tr');
    const actions = session && session.role === 'admin'
      ? `<button class="btn edit" data-id="${p.id}">Editar</button>
         <button class="btn delete" data-id="${p.id}">Eliminar</button>`
      : `<button class="btn add" data-id="${p.id}">Agregar al carrito</button>`;

    const imgSrc = p.image || PLACEHOLDER_IMG;
    const imgCell = `<td class="thumb"><img src="${imgSrc}" alt="${escapeHtml(p.name)}"></td>`;
    tr.innerHTML = `
      ${imgCell}
      <td>${escapeHtml(p.name)}</td>
      <td>${escapeHtml(p.desc || '')}</td>
      <td>${Number(p.price).toFixed(2)}</td>
      <td class="actions">${actions}</td>
    `;
    tbody.appendChild(tr);
  });
}

function escapeHtml(s){ return String(s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":"&#39;"})[c]); }

document.addEventListener('DOMContentLoaded', () => {
  updateAuthUI();
  updateCartUI();
  renderProducts('');

  const search = document.getElementById('search');
  search.addEventListener('input', renderProducts);

  const tbody = document.querySelector('#usersTable tbody');
  tbody.addEventListener('click', (e) => {
    const btn = e.target.closest('button');
    if (!btn) return;
    const id = btn.dataset.id;
    if (btn.classList.contains('edit')) {
      window.location.href = `Editar.html?id=${encodeURIComponent(id)}`;
      return;
    }
    if (btn.classList.contains('delete')) {
      if (!confirm('¿Eliminar este producto?')) return;
      const items = getProducts().filter(u => u.id !== id);
      saveProducts(items);
      renderProducts(search.value);
      return;
    }
    if (btn.classList.contains('add')) {
      addToCart(id);
      // show confirmation message instead of redirecting
      const product = getProducts().find(p => p.id === id);
      showMessage(`"${product.name}" agregado al carrito.`, 'success');
      updateCartUI();
      return;
    }
  });
});

function addToCart(productId) {
  const cartKey = 'pdj_cart';
  const raw = sessionStorage.getItem(cartKey);
  const cart = raw ? JSON.parse(raw) : [];
  const existing = cart.find(i => i.productId === productId);
  if (existing) existing.qty += 1; else cart.push({ productId, qty: 1 });
  sessionStorage.setItem(cartKey, JSON.stringify(cart));
}

function updateCartUI() {
  const cartKey = 'pdj_cart';
  const raw = sessionStorage.getItem(cartKey);
  const cart = raw ? JSON.parse(raw) : [];
  const totalItems = cart.reduce((sum, item) => sum + item.qty, 0);
  const cartCountSpan = document.getElementById('cartCount');
  if (cartCountSpan) cartCountSpan.textContent = totalItems;
}
