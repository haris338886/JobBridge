/* ============================================================
   JobBridge — Marketing pages
   ============================================================ */
(function (window, document) {
    'use strict';

    function initSearch() {
        const form = document.querySelector('.hero-search');
        if (!form) return;
        form.querySelectorAll('input').forEach(input => {
            input.addEventListener('keydown', e => {
                if (e.key === 'Enter') { e.preventDefault(); form.submit(); }
            });
        });
    }

    function initJobFilters() {
        const form = document.querySelector('.job-filter-form');
        if (!form) return;
        form.querySelectorAll('input, select').forEach(input => {
            input.addEventListener('change', () => form.submit());
        });
    }

    function initSaveJobButtons() {
        document.querySelectorAll('[data-save-job]').forEach(btn => {
            btn.addEventListener('click', (e) => {
                const id = btn.dataset.saveJob;
                if (!id) return;
                e.preventDefault();
                if (!window.JobBridge?.api?.jobs?.save) return;
                window.JobBridge.api.jobs.save(id)
                    .then(() => {
                        window.JobBridge.notifications?.show('Job saved', 'success');
                        btn.textContent = 'Saved';
                        btn.disabled = true;
                    })
                    .catch((err) => {
                        window.JobBridge.notifications?.show(
                            err?.message || 'Could not save job', 'error'
                        );
                    });
            });
        });
    }

    function init() {
        initSearch();
        initJobFilters();
        initSaveJobButtons();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);