/*
  Crear.JS — Lógica de gestión de productos (crear, actualizar, eliminar).
  Copiado desde la implementación previa y adaptado al nuevo nombre de fichero (Crear.JS).
  Usa localStorage (`pdj_products_v1`) para persistencia y sessionStorage para sesión.
*/
(function(){
  'use strict';

  const STORAGE_KEY = 'pdj_products_v1';
  const SESSION_KEY = 'crud_current_user';

  function getProducts(){
    try{ return JSON.parse(localStorage.getItem(STORAGE_KEY) || '[]'); }
    catch(e){ return []; }
  }

  function saveProducts(products){
    localStorage.setItem(STORAGE_KEY, JSON.stringify(products));
  }

  function qs(id){ return document.getElementById(id); }

  function getSession(){
    try{ return JSON.parse(sessionStorage.getItem(SESSION_KEY)); }
    catch(e){ return null; }
  }

  function updateAuthUI(){
    const auth = qs('authActions');
    const me = getSession();
    if(!auth) return;
    auth.innerHTML = '';
    if(me){
      const span = document.createElement('span');
      span.textContent = `${me.name} (${me.role || 'user'})`;
      const logout = document.createElement('button');
      logout.className = 'btn';
      logout.textContent = 'Cerrar Sesión';
      logout.addEventListener('click', ()=>{ sessionStorage.removeItem(SESSION_KEY); window.location.href='Index.html'; });
      auth.appendChild(span);
      auth.appendChild(logout);
    } else {
      const login = document.createElement('a');
      login.href = 'Index.html';
      login.className = 'btn';
      login.textContent = 'Iniciar sesión';
      auth.appendChild(login);
    }
  }

  function readFileAsDataURL(file){
    return new Promise((res,rej)=>{
      const fr = new FileReader();
      fr.onload = ()=>res(fr.result);
      fr.onerror = rej;
      fr.readAsDataURL(file);
    });
  }

  function init(){
    updateAuthUI();

    const me = getSession();
    if(!me || me.role !== 'admin'){
      const note = document.createElement('p');
      note.className = 'muted';
      note.textContent = 'Acceso de gestor restringido: inicie sesión como administrador.';
      document.querySelector('.form-section').appendChild(note);
    }

    const imageInput = qs('productImage');
    const chooseBtn = qs('chooseImageBtn');
    const preview = qs('productPreview');

    chooseBtn && chooseBtn.addEventListener('click', ()=> imageInput.click());
    imageInput && imageInput.addEventListener('change', async (ev)=>{
      const file = ev.target.files[0];
      if(!file) return;
      if(file.size > 200000){ alert('Imagen demasiado grande (máx 200KB).'); return; }
      try{ const data = await readFileAsDataURL(file); preview.src = data; preview.style.display='block'; }
      catch(e){ console.error(e); }
    });

    const form = qs('productForm');
    form && form.addEventListener('submit', async (e)=>{
      e.preventDefault();
      const id = qs('productId').value || null;
      const name = qs('productName').value.trim();
      const desc = qs('productDesc').value.trim();
      const price = parseFloat(qs('productPrice').value) || 0;
      const stock = parseInt(qs('productStock').value) || 0;
      let image = preview.src || null;

      const products = getProducts();
      if(id){
        const idx = products.findIndex(p=>p.id===id);
        if(idx>=0){ products[idx] = { ...products[idx], name, desc, price, stock, image }; }
      } else {
        products.push({ id: 'p_'+Date.now(), name, desc, price, stock, image });
      }
      saveProducts(products);
      alert('Producto guardado.');
      window.location.href = 'Lista.html';
    });

    qs('cancelBtn') && qs('cancelBtn').addEventListener('click', ()=> window.location.href='Lista.html');
  }

  document.addEventListener('DOMContentLoaded', init);
})();
