/* ============================================================
   JobBridge — Employer dashboard
   ============================================================ */
(function (window, document) {
    'use strict';

    function initJobForm() {
        const form = document.querySelector('form[action*="create-job"], form[action*="edit-job"]');
        if (!form) return;
        form.addEventListener('submit', e => {
            const required = form.querySelectorAll('[required]');
            let ok = true;
            required.forEach(field => {
                if (!field.value.trim()) {
                    ok = false;
                    window.JobBridge.validation.markError(field, 'Required');
                }
            });
            if (!ok) {
                e.preventDefault();
                window.JobBridge.notifications.show('Please fill all required fields', 'warning');
            }
        });
    }

    function initApplicantActions() {
        document.querySelectorAll('[data-applicant-action]').forEach(btn => {
            btn.addEventListener('click', async e => {
                e.preventDefault();
                const { applicantAction, applicantId } = btn.dataset;
                if (!confirm(`Are you sure you want to ${applicantAction}?`)) return;
                try {
                    await window.JobBridge.api.post(
                        `/api/applications/${applicantId}/${applicantAction}/`,
                        {}
                    );
                    window.JobBridge.notifications.show(`Applicant ${applicantAction}ed`, 'success');
                    setTimeout(() => window.location.reload(), 800);
                } catch (err) {
                    window.JobBridge.notifications.show(err.message, 'error');
                }
            });
        });
    }

    function init() {
        initJobForm();
        initApplicantActions();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);