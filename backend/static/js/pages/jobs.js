/* ============================================================
   JobBridge — Job listing & detail page behaviours
   ============================================================ */
(function (window, document) {
    'use strict';

    /* ---------- Filter sidebar toggles on mobile ---------- */
    function initFilterToggle() {
        const toggle = document.querySelector('[data-toggle-filters]');
        const panel = document.querySelector('[data-filters-panel]');
        if (!toggle || !panel) return;
        toggle.addEventListener('click', () => {
            panel.classList.toggle('open');
            toggle.setAttribute('aria-expanded', String(panel.classList.contains('open')));
        });
    }

    /* ---------- Auto-submit filter form on change ---------- */
    function initFilterAutoSubmit() {
        const form = document.querySelector('[data-filter-form]');
        if (!form) return;
        form.querySelectorAll('input[type="checkbox"], input[type="radio"], select').forEach(el => {
            el.addEventListener('change', () => form.submit());
        });
    }

    /* ---------- Save job (list + detail) ---------- */
    function initSaveJob() {
        document.querySelectorAll('[data-save-job]').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                e.preventDefault();
                const id = btn.dataset.saveJob;
                if (!id) return;

                const api = window.JobBridge?.api?.jobs?.save;
                if (!api) {
                    window.JobBridge?.notifications?.show('Please log in to save jobs.', 'warning');
                    return;
                }
                btn.disabled = true;
                try {
                    await api(id);
                    btn.classList.add('saved');
                    const label = btn.querySelector('.js-save-label');
                    if (label) label.textContent = 'Saved';
                    window.JobBridge?.notifications?.show('Job saved', 'success');
                } catch (err) {
                    btn.disabled = false;
                    window.JobBridge?.notifications?.show(
                        err?.message || 'Could not save job.', 'error'
                    );
                }
            });
        });
    }

    /* ---------- Apply Now — POST to application API ---------- */
    function initApplyNow() {
        const form = document.getElementById('applyForm');
        if (!form) return;

        const alertEl = document.getElementById('applyAlert');
        const submit = form.querySelector('button[type="submit"]');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (alertEl) alertEl.className = 'auth-alert';

            const jobId = form.dataset.jobId;
            if (!jobId) return;

            submit.classList.add('is-loading');
            submit.disabled = true;

            try {
                const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
                const res = await fetch('/applications/api/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': csrf,
                        'X-Requested-With': 'XMLHttpRequest',
                    },
                    body: JSON.stringify({
                        job: Number(jobId),
                        cover_letter: form.cover_letter?.value?.trim() || '',
                    }),
                });
                const data = await res.json().catch(() => ({}));

                if (!res.ok) {
                    const msg = data?.detail
                        || (data?.errors && Object.values(data.errors)[0])
                        || 'Could not submit application.';
                    if (alertEl) {
                        alertEl.textContent = typeof msg === 'string' ? msg : 'Could not submit application.';
                        alertEl.className = 'auth-alert show error';
                    }
                    return;
                }

                if (alertEl) {
                    alertEl.textContent = 'Application submitted! Redirecting…';
                    alertEl.className = 'auth-alert show success';
                }
                setTimeout(() => { window.location.href = '/candidate/applications/'; }, 900);
            } catch (err) {
                if (alertEl) {
                    alertEl.textContent = 'Network error. Please try again.';
                    alertEl.className = 'auth-alert show error';
                }
            } finally {
                submit.classList.remove('is-loading');
                submit.disabled = false;
            }
        });
    }

    /* ---------- Share button (copy link) ---------- */
    function initShare() {
        document.querySelectorAll('[data-share]').forEach(btn => {
            btn.addEventListener('click', async () => {
                const url = window.location.href;
                try {
                    if (navigator.share) {
                        await navigator.share({ title: document.title, url });
                    } else {
                        await navigator.clipboard.writeText(url);
                        window.JobBridge?.notifications?.show('Link copied to clipboard.', 'success');
                    }
                } catch (_) { /* user cancelled */ }
            });
        });
    }

    function init() {
        initFilterToggle();
        initFilterAutoSubmit();
        initSaveJob();
        initApplyNow();
        initShare();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);