/* ============================================================
   JobBridge — Contact page (form submit + FAQ accordion)
   ============================================================ */
(function (window, document) {
    'use strict';

    function initFaq() {
        document.querySelectorAll('.faq-item').forEach(item => {
            const header = item.querySelector('.faq-header');
            if (!header) return;
            header.addEventListener('click', () => {
                const open = !item.classList.contains('open');
                // close others (single-open)
                document.querySelectorAll('.faq-item.open').forEach(o => {
                    if (o !== item) o.classList.remove('open');
                });
                item.classList.toggle('open', open);
            });
        });
    }

    function initContactForm() {
        const form = document.getElementById('contactForm');
        if (!form) return;
        const alertEl = document.getElementById('contactAlert');
        const btn = form.querySelector('button[type="submit"]');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            if (alertEl) alertEl.className = 'auth-alert';

            const data = {
                name:    form.name.value.trim(),
                email:   form.email.value.trim(),
                subject: form.subject.value.trim(),
                inquiry: form.inquiry.value,
                message: form.message.value.trim(),
            };

            if (!data.name || !data.email || !data.subject || !data.message) {
                if (alertEl) {
                    alertEl.textContent = 'Please fill in all required fields.';
                    alertEl.className = 'auth-alert show error';
                }
                return;
            }

            btn.classList.add('is-loading');
            btn.disabled = true;

            try {
                const csrf = document.cookie.match(/csrftoken=([^;]+)/)?.[1] || '';
                const res = await fetch(window.location.href, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                        'X-CSRFToken': csrf,
                    },
                    body: new URLSearchParams({
                        name: data.name,
                        email: data.email,
                        subject: data.subject,
                        inquiry: data.inquiry,
                        message: data.message,
                    }),
                });
                if (!res.ok) throw new Error('Request failed');
                window.location.reload();
            } catch (err) {
                if (alertEl) {
                    alertEl.textContent = 'Could not send your message. Please try again.';
                    alertEl.className = 'auth-alert show error';
                }
            } finally {
                btn.classList.remove('is-loading');
                btn.disabled = false;
            }
        });
    }

    function init() {
        initFaq();
        initContactForm();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);