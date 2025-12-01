/*
 * Carrito.js — Maneja la experiencia del carrito de compras.
 * Responsable de: leer el carrito desde sessionStorage (`pdj_cart`), renderizar tabla de items,
 * actualizar cantidades, eliminar items, vaciar carrito y simular checkout.
 * También muestra estado de sesión en el header.
 */

// Carrito.js — maneja el carrito en sessionStorage
const PRODUCTS_KEY = 'pdj_products_v1';
const CART_KEY = 'pdj_cart';
const SESSION_KEY = 'crud_current_user';

// placeholder SVG used when no product image is available
const _SVG_PLACEHOLDER = `<svg xmlns='http://www.w3.org/2000/svg' width='64' height='64'><rect width='100%' height='100%' fill='%23e6e9ef'/><text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle' fill='%239ca3af' font-size='11'>No image</text></svg>`;
const PLACEHOLDER_IMG = 'data:image/svg+xml;utf8,' + encodeURIComponent(_SVG_PLACEHOLDER);

function getProducts() { try { const r = localStorage.getItem(PRODUCTS_KEY); return r ? JSON.parse(r) : []; } catch(e){return[];} }
function getCart() { try { const r = sessionStorage.getItem(CART_KEY); return r ? JSON.parse(r) : []; } catch(e){return[]} }
function saveCart(cart) { sessionStorage.setItem(CART_KEY, JSON.stringify(cart)); }
function getSession(){ const r = sessionStorage.getItem(SESSION_KEY); return r?JSON.parse(r):null }

function updateAuthUI(){ const authActions=document.getElementById('authActions'); const user=getSession(); if(!authActions) return; if(user){ authActions.innerHTML = `<span class="muted">Bienvenido, ${user.name}</span><button id="logoutBtn" class="btn" style="margin-left:8px">Cerrar Sesión</button>`; const btn=document.getElementById('logoutBtn'); if(btn) btn.addEventListener('click',()=>{ sessionStorage.removeItem(SESSION_KEY); window.location.href='Index.html'; }); } else authActions.innerHTML=''; }

function renderCart(){ const cart=getCart(); const products=getProducts(); const tbody=document.querySelector('#cartTable tbody'); const emptyMessage=document.getElementById('emptyMessage'); const totalEl=document.getElementById('total'); tbody.innerHTML=''; if(!cart.length){ emptyMessage.style.display='block'; totalEl.textContent='0.00'; return; } emptyMessage.style.display='none'; let total=0; cart.forEach(item=>{ const p=products.find(x=>x.id===item.productId); if(!p) return; const subtotal = (Number(p.price)||0) * item.qty; total+=subtotal; const tr=document.createElement('tr'); const imgSrc = p.image || PLACEHOLDER_IMG; tr.innerHTML = `<td class="thumb"><img src="${imgSrc}" alt="${p.name}" style="max-width:60px;border-radius:4px;"></td><td>${p.name}</td><td>$${Number(p.price).toFixed(2)}</td><td><input class="qty" data-id="${p.id}" type="number" min="1" value="${item.qty}"></td><td>$${subtotal.toFixed(2)}</td><td><button class="remove" data-id="${p.id}">Eliminar</button></td>`; tbody.appendChild(tr); }); totalEl.textContent = total.toFixed(2); }

document.addEventListener('DOMContentLoaded', ()=>{
  updateAuthUI();
  renderCart();
  const tbody=document.querySelector('#cartTable tbody');
  tbody.addEventListener('input', (e)=>{
    if(e.target.classList.contains('qty')){
      const id=e.target.dataset.id; const val=parseInt(e.target.value,10)||1; const cart=getCart(); const entry=cart.find(i=>i.productId===id); if(entry){ entry.qty=val; saveCart(cart); renderCart(); }
    }
  });

  tbody.addEventListener('click',(e)=>{
    const btn=e.target.closest('button'); if(!btn) return; const id=btn.dataset.id; if(btn.classList.contains('remove')){ let cart=getCart(); cart=cart.filter(i=>i.productId!==id); saveCart(cart); renderCart(); }
  });

  document.getElementById('clearBtn').addEventListener('click',()=>{ if(confirm('Vaciar carrito?')){ saveCart([]); renderCart(); } });
  document.getElementById('checkoutBtn').addEventListener('click',()=>{
    if(!getCart().length){ showMessage('Carrito vacío.', 'warning'); return; }
    // Simular checkout
    showMessage('Gracias por tu compra. Carrito vaciado.', 'success');
    saveCart([]);
    renderCart();
  });
});
