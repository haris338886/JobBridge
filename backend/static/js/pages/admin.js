/* ============================================================
   JobBridge — Admin panel
   ============================================================ */
(function (window, document) {
    'use strict';

    function initConfirmations() {
        document.querySelectorAll('[data-confirm]').forEach(el => {
            el.addEventListener('click', e => {
                if (!confirm(el.dataset.confirm)) e.preventDefault();
            });
        });
    }

    function initUserActions() {
        document.querySelectorAll('[data-user-action]').forEach(btn => {
            btn.addEventListener('click', async e => {
                e.preventDefault();
                const { userAction, userId } = btn.dataset;
                try {
                    await window.JobBridge.api.post(
                        `/api/admin/users/${userId}/${userAction}/`,
                        {}
                    );
                    window.JobBridge.notifications.show(`User ${userAction}d`, 'success');
                } catch (err) {
                    window.JobBridge.notifications.show(err.message, 'error');
                }
            });
        });
    }

    function initFilters() {
        const form = document.querySelector('.admin-filters');
        if (!form) return;
        form.querySelectorAll('select').forEach(sel => {
            sel.addEventListener('change', () => form.submit());
        });
    }

    function init() {
        initConfirmations();
        initUserActions();
        initFilters();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);