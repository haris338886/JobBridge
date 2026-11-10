/* ============================================================
   JobBridge — Legal pages (scrollspy + back-to-top)
   ============================================================ */
(function (window, document) {
    'use strict';

    function initScrollspy() {
        const links = document.querySelectorAll('.legal-toc a[href^="#"]');
        if (!links.length) return;

        const sections = Array.from(links).map(link => ({
            link,
            section: document.getElementById(link.getAttribute('href').slice(1)),
        })).filter(x => x.section);

        if (!sections.length) return;

        const onScroll = () => {
            const offset = window.scrollY + 120;
            let active = sections[0];
            sections.forEach(item => {
                if (item.section.offsetTop <= offset) active = item;
            });
            links.forEach(l => l.classList.remove('active'));
            active?.link.classList.add('active');
        };

        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    function initBackToTop() {
        const btn = document.getElementById('backToTop');
        if (!btn) return;
        const toggle = () => {
            btn.classList.toggle('visible', window.scrollY > 400);
        };
        window.addEventListener('scroll', toggle, { passive: true });
        btn.addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
        toggle();
    }

    function init() {
        initScrollspy();
        initBackToTop();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);