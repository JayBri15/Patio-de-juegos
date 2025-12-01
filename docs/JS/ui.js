/* UI para notificaciones inline */
function showMessage(text, type = 'info', timeout = 3500) {
  const container = document.getElementById('pdj_message');
  if (!container) {
    console.warn('pdj_message container not found. Message:', text);
    return;
  }
  container.textContent = text;
  container.className = 'pdj-message ' + (type || 'info');
  container.style.display = 'block';
  if (timeout && timeout > 0) {
    clearTimeout(container._pdjTimeout);
    container._pdjTimeout = setTimeout(() => {
      container.style.display = 'none';
      container.textContent = '';
      container.className = 'pdj-message';
    }, timeout);
  }
}

function clearMessage() {
  const container = document.getElementById('pdj_message');
  if (!container) return;
  clearTimeout(container._pdjTimeout);
  container.style.display = 'none';
  container.textContent = '';
  container.className = 'pdj-message';
}

// Export for module systems (optional)
if (typeof window !== 'undefined') {
  window.showMessage = showMessage;
  window.clearMessage = clearMessage;
}
