/* ============================================================
   JobBridge — Reusable components
   ============================================================ */
(function (window, document) {
    'use strict';

    const components = {
        initAll() {
            this.initModals();
            this.initTabs();
            this.initDropdowns();
            this.initAccordions();
        },

        initModals() {
            document.querySelectorAll('[data-modal-open]').forEach(trigger => {
                trigger.addEventListener('click', () => {
                    const id = trigger.dataset.modalOpen;
                    const modal = document.querySelector(`[data-modal="${id}"]`);
                    if (modal) {
                        modal.classList.add('active');
                        document.body.style.overflow = 'hidden';
                    }
                });
            });

            document.querySelectorAll('[data-modal-close]').forEach(btn => {
                btn.addEventListener('click', () => {
                    btn.closest('.modal-backdrop')?.classList.remove('active');
                    document.body.style.overflow = '';
                });
            });

            document.querySelectorAll('.modal-backdrop').forEach(bd => {
                bd.addEventListener('click', e => {
                    if (e.target === bd) {
                        bd.classList.remove('active');
                        document.body.style.overflow = '';
                    }
                });
            });

            document.addEventListener('keydown', e => {
                if (e.key === 'Escape') {
                    document.querySelectorAll('.modal-backdrop.active')
                        .forEach(m => m.classList.remove('active'));
                    document.body.style.overflow = '';
                }
            });
        },

        initTabs() {
            document.querySelectorAll('[data-tabs]').forEach(group => {
                const buttons = group.querySelectorAll('[data-tab]');
                const panels = group.querySelectorAll('[data-tab-panel]');
                buttons.forEach(btn => {
                    btn.addEventListener('click', () => {
                        buttons.forEach(b => b.classList.remove('active'));
                        panels.forEach(p => p.classList.add('hidden'));
                        btn.classList.add('active');
                        const target = group.querySelector(`[data-tab-panel="${btn.dataset.tab}"]`);
                        if (target) target.classList.remove('hidden');
                    });
                });
            });
        },

        initDropdowns() {
            document.querySelectorAll('[data-dropdown]').forEach(wrapper => {
                const trigger = wrapper.querySelector('[data-dropdown-trigger]');
                const menu = wrapper.querySelector('[data-dropdown-menu]');
                if (!trigger || !menu) return;
                trigger.addEventListener('click', e => {
                    e.stopPropagation();
                    menu.classList.toggle('hidden');
                });
                document.addEventListener('click', () => menu.classList.add('hidden'));
            });
        },

        initAccordions() {
            document.querySelectorAll('[data-accordion]').forEach(item => {
                const header = item.querySelector('[data-accordion-header]');
                const body = item.querySelector('[data-accordion-body]');
                if (!header || !body) return;
                header.addEventListener('click', () => {
                    body.classList.toggle('hidden');
                    item.classList.toggle('open');
                });
            });
        },
    };

    window.JobBridge = window.JobBridge || {};
    window.JobBridge.components = components;
})(window, document);