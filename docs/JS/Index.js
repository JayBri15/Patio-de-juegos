/*
 * Index.js — Manejo de autenticación en cliente.
 * Responsable de: registro de usuarios (hash SHA-256), inicio de sesión,
 * almacenamiento de usuarios en localStorage (`crud_users_v1`), manejo de sesión
 * en sessionStorage (`crud_current_user`) y actualización de la UI según sesión.
 */

// Lógica de registro/inicio de sesión separada
const STORAGE_KEY = 'crud_users_v1';
const SESSION_KEY = 'crud_current_user';

// DOM
const tabLogin = document.getElementById('tabLogin');
const tabRegister = document.getElementById('tabRegister');
const loginForm = document.getElementById('loginForm');
const registerForm = document.getElementById('registerForm');

const loginName = document.getElementById('loginName');
const loginPassword = document.getElementById('loginPassword');
const regName = document.getElementById('regName');
const regEmail = document.getElementById('regEmail');
const regPassword = document.getElementById('regPassword');
const regPassword2 = document.getElementById('regPassword2');

function getUsers() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    return raw ? JSON.parse(raw) : [];
  } catch (e) {
    console.error(e);
    return [];
  }
}

function saveUsers(users) {
  localStorage.setItem(STORAGE_KEY, JSON.stringify(users));
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).slice(2, 8);
}

async function hashPassword(password) {
  const enc = new TextEncoder();
  const data = enc.encode(password);
  const hashBuffer = await crypto.subtle.digest('SHA-256', data);
  return Array.from(new Uint8Array(hashBuffer)).map(b => b.toString(16).padStart(2, '0')).join('');
}

function setSession(user) {
  if (user) sessionStorage.setItem(SESSION_KEY, JSON.stringify(user));
  updateAuthUI();
}

function getSession() {
  const raw = sessionStorage.getItem(SESSION_KEY);
  return raw ? JSON.parse(raw) : null;
}

function clearSession() {
  sessionStorage.removeItem(SESSION_KEY);
  updateAuthUI();
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
      clearSession();
      // stay on this page and show login (reload ensures forms are reset)
      window.location.href = 'Index.html';
    });
    // if logged in, hide auth forms
    document.getElementById('authSection').style.display = 'none';
  } else {
    authActions.innerHTML = '';
    // show auth forms when no session
    const authSection = document.getElementById('authSection');
    if (authSection) authSection.style.display = '';
    // ensure login tab shown
    tabLogin && tabLogin.classList.add('active');
    tabRegister && tabRegister.classList.remove('active');
    loginForm && (loginForm.style.display = '');
    registerForm && (registerForm.style.display = 'none');
  }
}

// Tab switching
tabLogin.addEventListener('click', () => {
  tabLogin.classList.add('active');
  tabRegister.classList.remove('active');
  loginForm.style.display = '';
  registerForm.style.display = 'none';
});
tabRegister.addEventListener('click', () => {
  tabRegister.classList.add('active');
  tabLogin.classList.remove('active');
  registerForm.style.display = '';
  loginForm.style.display = 'none';
});

// Register
registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const name = regName.value.trim();
  const email = regEmail.value.trim().toLowerCase();
  const pw = regPassword.value;
  const pw2 = regPassword2.value;

  if (!name || !email || !pw || !pw2) return showMessage('Completa todos los campos.', 'error');
  if (pw !== pw2) return showMessage('Las contraseñas no coinciden.', 'error');

  const users = getUsers();
  if (users.find(u => u.email.toLowerCase() === email)) return showMessage('Ya existe un usuario con ese correo.', 'error');

  const pwHash = await hashPassword(pw);
  const user = { id: generateId(), name, email, passwordHash: pwHash, role: 'user' };
  users.push(user);
  saveUsers(users);
  showMessage('Registro exitoso. Ahora inicia sesión.', 'success');
  tabLogin.click();
  registerForm.reset();
});

// Login
loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  const loginUserName = loginName.value.trim();
  const pw = loginPassword.value;
  if (!loginUserName || !pw) return showMessage('Completa nombre de usuario y contraseña.', 'error');

  // admin special case: username 'admin' and password '123'
  if (loginUserName === 'admin' && pw === '123') {
    const admin = { id: 'admin', name: 'Administrator', email: 'admin', role: 'admin' };
    setSession(admin);
    setTimeout(() => { window.location.href = 'Crear.html'; }, 150);
    return;
  }

  const users = getUsers();
  // match by username (name) — case-insensitive
  const user = users.find(u => (u.name || '').toLowerCase() === loginUserName.toLowerCase());
  if (!user) return showMessage('Usuario no encontrado.', 'error');
  if (!user.passwordHash) return showMessage('Usuario sin contraseña. Regístrate.', 'error');
  const pwHash = await hashPassword(pw);
  if (pwHash !== user.passwordHash) return showMessage('Contraseña incorrecta.', 'error');

  // success: set session and redirect to product list
  const sessionUser = { id: user.id, name: user.name, email: user.email, role: user.role || 'user' };
  setSession(sessionUser);
  setTimeout(() => { window.location.href = 'Lista.html'; }, 150);
});

// Inicializar vista según sesión
document.addEventListener('DOMContentLoaded', () => {
  updateAuthUI();
});
