/* ============================================================
   JobBridge — Auth page behaviours
   (password toggle, strength meter, form submit, JWT login)
   ============================================================ */
(function (window, document) {
    'use strict';

    /* ---------- Password visibility toggle ---------- */
    function initPasswordToggles() {
        document.querySelectorAll('.password-toggle').forEach(btn => {
            btn.addEventListener('click', () => {
                const input = btn.parentElement.querySelector('input');
                if (!input) return;
                const showing = input.type === 'text';
                input.type = showing ? 'password' : 'text';
                btn.setAttribute('aria-label', showing ? 'Show password' : 'Hide password');
                btn.innerHTML = showing
                    ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>'
                    : '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"/><line x1="1" y1="1" x2="23" y2="23"/></svg>';
            });
        });
    }

    /* ---------- Password strength meter ---------- */
    function scorePassword(pw) {
        let score = 0;
        if (pw.length >= 8)  score++;
        if (/[A-Z]/.test(pw) && /[a-z]/.test(pw)) score++;
        if (/\d/.test(pw)) score++;
        if (/[^A-Za-z0-9]/.test(pw)) score++;
        return score;
    }

    function initStrengthMeters() {
        document.querySelectorAll('[data-strength-for]').forEach(meter => {
            const input = document.getElementById(meter.dataset.strengthFor);
            if (!input) return;
            const label = meter.nextElementSibling;
            input.addEventListener('input', () => {
                const s = scorePassword(input.value);
                meter.setAttribute('data-strength', String(s));
                if (label) {
                    const map = ['', 'Weak', 'Fair', 'Good', 'Strong'];
                    label.textContent = input.value ? map[s] : '';
                    label.style.color = s <= 1 ? 'var(--danger-600)'
                                     : s === 2 ? 'var(--warning-600)'
                                     : s === 3 ? 'var(--blue-600)'
                                     : 'var(--success-600)';
                }
            });
        });
    }

    /* ---------- Alert helper ---------- */
    function showAlert(el, message, type = 'error') {
        if (!el) return;
        el.textContent = message;
        el.className = `auth-alert show ${type}`;
        el.style.display = 'block'; // Ensure visibility
    }
    function hideAlert(el) {
        if (!el) return;
        el.className = 'auth-alert';
        el.style.display = 'none'; // Ensure invisibility
    }

    /* ---------- API fetch helper ---------- */
    async function apiPost(path, body) {
        // Fallback to empty string if config doesn't exist
        const base = window.JobBridge?.config?.apiBase || '';
        const csrf = getCookie('csrftoken');
        
        // Ensure path starts with a slash
        const url = path.startsWith('/') ? path : '/' + path;

        const res = await fetch(base + url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrf,
                'X-Requested-With': 'XMLHttpRequest',
            },
            body: JSON.stringify(body),
        });
        const data = await res.json().catch(() => ({}));
        return { ok: res.ok, status: res.status, data };
    }

    function getCookie(name) {
        const m = document.cookie.match(new RegExp('(^|;\\s*)' + name + '=([^;]*)'));
        return m ? decodeURIComponent(m[2]) : '';
    }

    /* ---------- LOGIN form ---------- */
    function initLoginForm() {
        const form = document.getElementById('loginForm');
        if (!form) return;

        const alertEl = document.getElementById('loginAlert');
        const submit = form.querySelector('button[type="submit"]');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert(alertEl);

            const email    = form.identifier.value.trim();
            const password = form.password.value;

            if (!email || !password) {
                showAlert(alertEl, 'Please fill in all fields.');
                return;
            }

            submit.classList.add('is-loading');
            submit.disabled = true;

            try {
                const { ok, status, data } = await apiPost('/accounts/api/login/', {
                    identifier: email,
                    password: password,
                });

                if (!ok) {
                    const msg = data?.detail
                        || (data?.errors && Object.values(data.errors)[0])
                        || 'Invalid email or password.';
                    showAlert(alertEl, typeof msg === 'string' ? msg : 'Invalid credentials.');
                    return;
                }

                if (data.tokens && window.JobBridge?.auth?.saveTokens) {
                    window.JobBridge.auth.saveTokens(data.tokens.access, data.tokens.refresh);
                }

                const role = data?.user?.role;
                const redirects = {
                    candidate: '/candidate/',
                    employer:  '/employer/',
                    admin:     '/admin/',
                };
                window.location.href = redirects[role] || '/';
            } catch (err) {
                showAlert(alertEl, 'Network error. Please check your connection.');
                console.error('[Login Error]', err);
            } finally {
                submit.classList.remove('is-loading');
                submit.disabled = false;
            }
        });
    }

    /* ---------- REGISTER forms ---------- */
    function initRegisterForm(formId) {
        const form = document.getElementById(formId);
        if (!form) return;

        const alertEl = document.getElementById('registerAlert');
        const submit = form.querySelector('button[type="submit"]');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            hideAlert(alertEl);

            const p1 = form.password.value;
            const p2 = form.password_confirm.value;
            if (p1 !== p2) {
                showAlert(alertEl, 'Passwords do not match.');
                return;
            }
            if (p1.length < 8) {
                showAlert(alertEl, 'Password must be at least 8 characters.');
                return;
            }
            if (!form.terms.checked) {
                showAlert(alertEl, 'Please accept the Terms and Privacy Policy.');
                return;
            }

            submit.classList.add('is-loading');
            submit.disabled = true;

            try {
                const body = {
                    email: form.email.value.trim(),
                    password: p1,
                    password_confirm: p2,
                    first_name: form.first_name.value.trim(),
                    last_name: form.last_name.value.trim(),
                    role: formId === 'registerEmployerForm' ? 'employer' : 'candidate',
                };
                
                // Include username if the field exists (some setups require it)
                if (form.username) body.username = form.username.value.trim();

                const { ok, data } = await apiPost('/accounts/api/register/', body);

                if (!ok) {
                    let msg = 'Registration failed.';
                    if (data && typeof data === 'object') {
                        if (data.errors) {
                            const first = Object.values(data.errors)[0];
                            msg = Array.isArray(first) ? first[0] : String(first);
                        } else if (data.detail) {
                            msg = data.detail;
                        }
                    }
                    showAlert(alertEl, msg);
                    return;
                }

                if (data.tokens && window.JobBridge?.auth?.saveTokens) {
                    window.JobBridge.auth.saveTokens(data.tokens.access, data.tokens.refresh);
                }

                showAlert(alertEl, 'Account created! Redirecting…', 'success');
                const role = data?.user?.role;
                const dest = role === 'employer' ? '/employer/' : '/candidate/';
                setTimeout(() => { window.location.href = dest; }, 700);
            } catch (err) {
                showAlert(alertEl, 'Network error. Please check your connection.');
                console.error('[Register Error]', err);
            } finally {
                submit.classList.remove('is-loading');
                submit.disabled = false;
            }
        });
    }

    /* ---------- RESET PASSWORD ---------- */
    function initResetForm() {
        const requestForm = document.getElementById('resetRequestForm');
        const confirmForm = document.getElementById('resetConfirmForm');
        const alertEl = document.getElementById('resetAlert');

        if (requestForm) {
            requestForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                hideAlert(alertEl);
                const email = requestForm.email.value.trim();
                if (!email) {
                    showAlert(alertEl, 'Please enter your email address.');
                    return;
                }

                const btn = requestForm.querySelector('button[type="submit"]');
                btn.classList.add('is-loading');
                btn.disabled = true;

                try {
                    await apiPost('/accounts/api/password-reset/', { email });
                    showAlert(alertEl, 'If that email is registered, a reset link has been sent.', 'success');
                    requestForm.reset();
                } catch (err) {
                    showAlert(alertEl, 'Network error. Please try again.');
                } finally {
                    btn.classList.remove('is-loading');
                    btn.disabled = false;
                }
            });
        }

        if (confirmForm) {
            confirmForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                hideAlert(alertEl);

                const p1 = confirmForm.password.value;
                const p2 = confirmForm.password_confirm.value;
                if (p1 !== p2) {
                    showAlert(alertEl, 'Passwords do not match.');
                    return;
                }
                if (p1.length < 8) {
                    showAlert(alertEl, 'Password must be at least 8 characters.');
                    return;
                }

                const uidb64 = confirmForm.dataset.uid;
                const token  = confirmForm.dataset.token;
                if (!uidb64 || !token) {
                    showAlert(alertEl, 'Invalid or expired reset link.');
                    return;
                }

                const btn = confirmForm.querySelector('button[type="submit"]');
                btn.classList.add('is-loading');
                btn.disabled = true;

                try {
                    const { ok, data } = await apiPost(
                        '/accounts/api/password-reset/confirm/',
                        { token: `${uidb64}:${token}`, new_password: p1 }
                    );
                    if (!ok) {
                        const msg = data?.detail || 'Reset failed. The link may have expired.';
                        showAlert(alertEl, msg);
                        return;
                    }
                    showAlert(alertEl, 'Password updated. Redirecting to login…', 'success');
                    setTimeout(() => { window.location.href = '/accounts/login/'; }, 900);
                } catch (err) {
                    showAlert(alertEl, 'Network error. Please try again.');
                } finally {
                    btn.classList.remove('is-loading');
                    btn.disabled = false;
                }
            });
        }
    }

    /* ---------- Boot ---------- */
    function init() {
        initPasswordToggles();
        initStrengthMeters();
        initLoginForm();
        initRegisterForm('registerCandidateForm');
        initRegisterForm('registerEmployerForm');
        initResetForm();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})(window, document);