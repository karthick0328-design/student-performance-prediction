/**
 * AI-Based Student Performance Prediction System
 * Frontend Interactions, Theme Controller & Settings Modal
 */

(function () {
  'use strict';

  // SVG Icons
  const MOON_ICON = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/>
  </svg>`;

  const SUN_ICON = `<svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
    <circle cx="12" cy="12" r="5"/>
    <line x1="12" y1="1" x2="12" y2="3"/>
    <line x1="12" y1="21" x2="12" y2="23"/>
    <line x1="4.22" y1="4.22" x2="5.64" y2="5.64"/>
    <line x1="18.36" y1="18.36" x2="19.78" y2="19.78"/>
    <line x1="1" y1="12" x2="3" y2="12"/>
    <line x1="21" y1="12" x2="23" y2="12"/>
    <line x1="4.22" y1="19.78" x2="5.64" y2="18.36"/>
    <line x1="18.36" y1="5.64" x2="19.78" y2="4.22"/>
  </svg>`;

  /* ==========================================================
     Theme Controller
     ========================================================== */
  function getPreferredTheme() {
    try {
      const saved = localStorage.getItem('app_theme');
      if (saved === 'dark' || saved === 'light') return saved;
    } catch (e) {
      console.warn('localStorage access failed:', e);
    }
    return 'light'; // Default pure white theme
  }

  function applyTheme(theme) {
    const isDark = theme === 'dark';
    if (isDark) {
      document.documentElement.setAttribute('data-theme', 'dark');
    } else {
      document.documentElement.removeAttribute('data-theme');
    }

    try {
      localStorage.setItem('app_theme', theme);
    } catch (e) {
      console.warn('Could not save theme to localStorage:', e);
    }

    // Update Header Icon & Tooltip
    const iconSpan = document.getElementById('theme-icon');
    const toggleBtn = document.getElementById('theme-toggle-btn');
    if (iconSpan) {
      iconSpan.innerHTML = isDark ? SUN_ICON : MOON_ICON;
    }
    if (toggleBtn) {
      toggleBtn.setAttribute('title', isDark ? 'Switch to Light Theme' : 'Switch to Dark Theme');
    }

    // Update Modal Theme Switcher buttons
    const btnLight = document.getElementById('btn-theme-light');
    const btnDark = document.getElementById('btn-theme-dark');
    if (btnLight && btnDark) {
      if (isDark) {
        btnLight.classList.remove('active');
        btnDark.classList.add('active');
      } else {
        btnLight.classList.add('active');
        btnDark.classList.remove('active');
      }
    }

    // Update Chart.js themes dynamically if charts exist
    if (window.Chart) {
      const textColor = isDark ? '#cbd5e1' : '#64748b';
      const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.06)';
      Chart.defaults.color = textColor;
      Chart.defaults.borderColor = gridColor;

      if (Chart.instances) {
        Object.values(Chart.instances).forEach((chart) => {
          try {
            if (chart.options && chart.options.scales) {
              Object.values(chart.options.scales).forEach((scale) => {
                if (scale.ticks) scale.ticks.color = textColor;
                if (scale.title) scale.title.color = textColor;
                if (scale.grid) scale.grid.color = gridColor;
              });
            }
            if (chart.options && chart.options.plugins && chart.options.plugins.legend) {
              if (!chart.options.plugins.legend.labels) chart.options.plugins.legend.labels = {};
              chart.options.plugins.legend.labels.color = textColor;
            }
            chart.update();
          } catch (e) {}
        });
      }
    }
  }

  function toggleTheme() {
    const currentTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
    const nextTheme = currentTheme === 'dark' ? 'light' : 'dark';
    applyTheme(nextTheme);
  }

  /* ==========================================================
     Settings Modal Controller
     ========================================================== */
  function initSettingsModal() {
    const modal = document.getElementById('settings-modal');
    const openBtn = document.getElementById('settings-toggle-btn');
    const closeBtn = document.getElementById('modal-close-btn');
    const saveBtn = document.getElementById('modal-save-btn');
    const resetCacheBtn = document.getElementById('btn-reset-cache');
    const gradeScaleSelect = document.getElementById('setting-grade-scale');
    const guidanceCheckbox = document.getElementById('setting-guidance');

    if (!modal) return;

    function openModal() {
      // Load saved settings
      try {
        const savedScale = localStorage.getItem('app_grade_scale') || '20';
        const savedGuidance = localStorage.getItem('app_guidance') !== 'false';
        if (gradeScaleSelect) gradeScaleSelect.value = savedScale;
        if (guidanceCheckbox) guidanceCheckbox.checked = savedGuidance;
      } catch (e) {}

      // Sync theme buttons in modal
      const currentTheme = document.documentElement.getAttribute('data-theme') === 'dark' ? 'dark' : 'light';
      const btnLight = document.getElementById('btn-theme-light');
      const btnDark = document.getElementById('btn-theme-dark');
      if (btnLight && btnDark) {
        if (currentTheme === 'dark') {
          btnLight.classList.remove('active');
          btnDark.classList.add('active');
        } else {
          btnLight.classList.add('active');
          btnDark.classList.remove('active');
        }
      }

      modal.style.display = 'flex';
      document.body.style.overflow = 'hidden';
    }

    function closeModal() {
      modal.style.display = 'none';
      document.body.style.overflow = '';
    }

    function saveSettings() {
      try {
        if (gradeScaleSelect) {
          localStorage.setItem('app_grade_scale', gradeScaleSelect.value);
        }
        if (guidanceCheckbox) {
          localStorage.setItem('app_guidance', guidanceCheckbox.checked ? 'true' : 'false');
        }
      } catch (e) {}
      closeModal();
    }

    function resetCache() {
      if (confirm('Reset theme preferences and locally stored settings to default?')) {
        try {
          localStorage.removeItem('app_theme');
          localStorage.removeItem('app_grade_scale');
          localStorage.removeItem('app_guidance');
        } catch (e) {}
        applyTheme('light');
        if (gradeScaleSelect) gradeScaleSelect.value = '20';
        if (guidanceCheckbox) guidanceCheckbox.checked = true;
        closeModal();
      }
    }

    // Modal Events
    if (openBtn) openBtn.addEventListener('click', openModal);
    if (closeBtn) closeBtn.addEventListener('click', closeModal);
    if (saveBtn) saveBtn.addEventListener('click', saveSettings);
    if (resetCacheBtn) resetCacheBtn.addEventListener('click', resetCache);

    // Close when clicking on backdrop outside modal card
    modal.addEventListener('click', (e) => {
      if (e.target === modal) {
        closeModal();
      }
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
      if (e.key === 'Escape' && modal.style.display === 'flex') {
        closeModal();
      }
    });

    // Modal internal theme selector buttons
    const btnLight = document.getElementById('btn-theme-light');
    const btnDark = document.getElementById('btn-theme-dark');
    if (btnLight) {
      btnLight.addEventListener('click', () => applyTheme('light'));
    }
    if (btnDark) {
      btnDark.addEventListener('click', () => applyTheme('dark'));
    }
  }

  /* ==========================================================
     DOM Initializer
     ========================================================== */
  document.addEventListener('DOMContentLoaded', () => {
    // 1. Initialize Theme
    const activeTheme = getPreferredTheme();
    applyTheme(activeTheme);

    const themeToggleBtn = document.getElementById('theme-toggle-btn');
    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', toggleTheme);
    }

    // 2. Initialize Settings Modal
    initSettingsModal();

    // 3. Form Reset confirmation button on Predict Page
    const resetBtn = document.getElementById('reset-form-btn');
    const predictionForm = document.getElementById('prediction-form');

    if (resetBtn && predictionForm) {
      resetBtn.addEventListener('click', (e) => {
        e.preventDefault();
        if (confirm('Are you sure you want to reset the form fields to defaults?')) {
          window.location.href = '/predict';
        }
      });
    }

    // 4. Real-time Numeric Input Bounds Highlighting
    const numericInputs = document.querySelectorAll('input[type="number"]');
    numericInputs.forEach((input) => {
      input.addEventListener('input', () => {
        const min = parseFloat(input.getAttribute('min'));
        const max = parseFloat(input.getAttribute('max'));
        const val = parseFloat(input.value);

        if (!isNaN(val) && (val < min || val > max)) {
          input.style.borderColor = 'var(--danger)';
          input.style.backgroundColor = 'var(--danger-bg)';
        } else {
          input.style.borderColor = '';
          input.style.backgroundColor = '';
        }
      });
    });

    // 5. Mobile Sidebar Toggle
    const mobileToggleBtn = document.querySelector('.topbar-toggle');
    const sidebar = document.querySelector('.sidebar');
    if (mobileToggleBtn && sidebar) {
      mobileToggleBtn.addEventListener('click', () => {
        sidebar.classList.toggle('sidebar-mobile-open');
      });
    }
  });
})();
