/* ============================================================
   JobBridge — Register choice page
   ============================================================ */
(function (window, document) {
    'use strict';

    function initKeyboardNav() {
        const cards = document.querySelectorAll('.role-card');
        if (cards.length < 2) return;
        cards.forEach((card, index) => {
            card.addEventListener('keydown', (e) => {
                if (e.key === 'ArrowRight' || e.key === 'ArrowDown') {
                    e.preventDefault();
                    cards[(index + 1) % cards.length].focus();
                }
                if (e.key === 'ArrowLeft' || e.key === 'ArrowUp') {
                    e.preventDefault();
                    cards[(index - 1 + cards.length) % cards.length].focus();
                }
            });
        });
    }

    function initClickFeedback() {
        document.querySelectorAll('.role-card').forEach(card => {
            card.addEventListener('click', function () {
                card.style.pointerEvents = 'none';
                card.style.opacity = '0.9';
            });
        });
    }

    function initEntranceAnimation() {
        if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
        const cards = document.querySelectorAll('.role-card');
        cards.forEach((card, i) => {
            card.style.opacity = '0';
            card.style.transform = 'translateY(16px)';
            card.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
            setTimeout(() => {
                card.style.opacity = '1';
                card.style.transform = 'translateY(0)';
            }, 100 + i * 100);
        });
    }

    function init() {
        initKeyboardNav();
        initClickFeedback();
        initEntranceAnimation();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);