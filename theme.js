(() => {
  const root = document.documentElement;
  const storageKey = 'william-ford-theme';
  let theme = 'dark';

  // Apply a saved choice before the stylesheet loads to avoid a colour flash.
  try {
    if (localStorage.getItem(storageKey) === 'light') theme = 'light';
  } catch (_) {
    // The toggle still works when browser storage is unavailable.
  }
  root.dataset.theme = theme;

  document.addEventListener('DOMContentLoaded', () => {
    const button = document.querySelector('.theme-toggle');
    if (!button) return;

    const updateLabel = () => {
      const next = root.dataset.theme === 'dark' ? 'light' : 'dark';
      button.textContent = next === 'light' ? 'Light mode' : 'Dark mode';
      button.setAttribute('aria-label', `Switch to ${next} mode`);
    };

    updateLabel();
    button.hidden = false;
    button.addEventListener('click', () => {
      root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
      try {
        localStorage.setItem(storageKey, root.dataset.theme);
      } catch (_) {
        // Keep the selected theme for this page even without storage.
      }
      updateLabel();
    });
  });
})();
