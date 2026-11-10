/* ============================================================
   JobBridge — Boot (entry point on every page)
   ============================================================ */
(function (window, document) {
    'use strict';

    function initRevealAnimations() {
        const els = document.querySelectorAll('.reveal');
        if (!els.length) return;

        if (!('IntersectionObserver' in window)) {
            els.forEach(el => el.classList.add('visible'));
            return;
        }

        const io = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    io.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1, rootMargin: '0px 0px -40px 0px' });

        els.forEach(el => io.observe(el));
    }

    function initSidebarToggle() {
        const btn = document.querySelector('.topbar-menu-btn');
        const sidebar = document.querySelector('.sidebar');
        if (!btn || !sidebar) return;

        // Create backdrop if it doesn't exist
        let backdrop = document.querySelector('.sidebar-backdrop');
        if (!backdrop) {
            backdrop = document.createElement('div');
            backdrop.className = 'sidebar-backdrop';
            document.body.appendChild(backdrop);
        }

        const toggle = (open) => {
            sidebar.classList.toggle('open', open);
            backdrop.classList.toggle('active', open);
            document.body.style.overflow = open ? 'hidden' : '';
        };

        btn.addEventListener('click', () => {
            toggle(!sidebar.classList.contains('open'));
        });
        backdrop.addEventListener('click', () => toggle(false));

        document.addEventListener('keydown', (e) => {
            if (e.key === 'Escape') toggle(false);
        });
    }

    function initAlertDismiss() {
        document.querySelectorAll('.alert-close').forEach(btn => {
            btn.addEventListener('click', () => {
                const alert = btn.closest('.alert');
                if (!alert) return;
                alert.style.transition = 'opacity 0.2s, transform 0.2s';
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(20px)';
                setTimeout(() => alert.remove(), 200);
            });
        });
    }

    function initActiveNavLinks() {
        const path = window.location.pathname;
        document.querySelectorAll('.sidebar-link, .navbar-menu a').forEach(link => {
            const href = link.getAttribute('href');
            if (!href || href === '#') return;
            if (path === href || (href !== '/' && path.startsWith(href))) {
                link.classList.add('active');
            }
        });
    }

    function init() {
        if (window.JobBridge.components) window.JobBridge.components.initAll();
        if (window.JobBridge.navbar) window.JobBridge.navbar.init();
        if (window.JobBridge.footer) window.JobBridge.footer.init();

        initRevealAnimations();
        initSidebarToggle();
        initAlertDismiss();
        initActiveNavLinks();

        document.documentElement.classList.add('js-ready');
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);