/* ============================================================
   JobBridge — Footer
   ============================================================ */
(function (window, document) {
    'use strict';

    const footer = {
        init() {
            const yearEl = document.querySelector('[data-current-year]');
            if (yearEl) yearEl.textContent = new Date().getFullYear();
        },
    };

    window.JobBridge = window.JobBridge || {};
    window.JobBridge.footer = footer;
})(window, document);