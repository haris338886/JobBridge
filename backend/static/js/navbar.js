/* ============================================================
   JobBridge — Navbar (mobile menu toggle)
   ============================================================ */
(function (window, document) {
    'use strict';

    const navbar = {
        init() {
            const toggle = document.querySelector('.navbar-toggle');
            const menu = document.querySelector('.navbar-menu');
            if (!toggle || !menu) return;

            toggle.addEventListener('click', () => {
                const open = !menu.classList.contains('open');
                menu.classList.toggle('open', open);
                toggle.classList.toggle('open', open);
                toggle.setAttribute('aria-expanded', String(open));
            });

            // Close on link click
            menu.querySelectorAll('a').forEach(a => {
                a.addEventListener('click', () => {
                    menu.classList.remove('open');
                    toggle.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                });
            });

            // Close on outside click
            document.addEventListener('click', (e) => {
                if (!menu.contains(e.target) && !toggle.contains(e.target)) {
                    menu.classList.remove('open');
                    toggle.classList.remove('open');
                    toggle.setAttribute('aria-expanded', 'false');
                }
            });
        },
    };

    window.JobBridge = window.JobBridge || {};
    window.JobBridge.navbar = navbar;
})(window, document);