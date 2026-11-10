/* ============================================================
   JobBridge — Candidate dashboard
   ============================================================ */
(function (window, document) {
    'use strict';

    function initSkillAdd() {
        const form = document.querySelector('form[action*="skill"]');
        if (!form) return;
        form.addEventListener('submit', e => {
            const input = form.querySelector('input[name="skill"]');
            if (!input || !input.value.trim()) {
                e.preventDefault();
                window.JobBridge.notifications.show('Enter a skill', 'warning');
            }
        });
    }

    function initResumeUpload() {
        const input = document.querySelector('input[type="file"][name="resume"]');
        if (!input) return;
        input.addEventListener('change', () => {
            const file = input.files[0];
            if (!file) return;
            if (file.size > 5 * 1024 * 1024) {
                window.JobBridge.notifications.show('Resume must be under 5MB', 'error');
                input.value = '';
            }
        });
    }

    function initSaveJob() {
        document.querySelectorAll('[data-save-job]').forEach(btn => {
            btn.addEventListener('click', async e => {
                e.preventDefault();
                const jobId = btn.dataset.saveJob;
                try {
                    await window.JobBridge.api.jobs.save(jobId);
                    window.JobBridge.notifications.show('Job saved', 'success');
                    btn.textContent = 'Saved';
                    btn.disabled = true;
                } catch (err) {
                    window.JobBridge.notifications.show(err.message, 'error');
                }
            });
        });
    }

    function init() {
        initSkillAdd();
        initResumeUpload();
        initSaveJob();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);