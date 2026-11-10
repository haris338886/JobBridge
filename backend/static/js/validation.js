/* ============================================================
   JobBridge — Client-side form validation
   ============================================================ */
(function (window, document) {
    'use strict';

    const rules = {
        required(v) { return v !== null && v !== undefined && String(v).trim() !== ''; },
        email(v)    { return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(v); },
    };

    const validation = {
        init(formSelector = 'form[data-validate]') {
            document.querySelectorAll(formSelector).forEach(form => {
                form.addEventListener('submit', e => {
                    if (!this.validate(form)) {
                        e.preventDefault();
                        this.showErrors(form);
                    }
                });
                form.querySelectorAll('input, textarea, select').forEach(input => {
                    input.addEventListener('blur', () => this.validateField(input));
                });
            });
        },

        validate(form) {
            let ok = true;
            form.querySelectorAll('input[required], textarea[required], select[required]').forEach(field => {
                if (!field.value.trim()) { ok = false; this.markError(field, 'This field is required'); }
                else this.clearError(field);
            });
            const p1 = form.querySelector('input[name="password1"]');
            const p2 = form.querySelector('input[name="password2"]');
            if (p1 && p2 && p1.value !== p2.value) {
                ok = false;
                this.markError(p2, 'Passwords do not match');
            }
            return ok;
        },

        validateField(field) {
            if (field.hasAttribute('required') && !field.value.trim()) {
                this.markError(field, 'This field is required');
                return false;
            }
            if (field.type === 'email' && field.value && !rules.email(field.value)) {
                this.markError(field, 'Please enter a valid email');
                return false;
            }
            this.clearError(field);
            return true;
        },

        markError(field, msg) {
            field.classList.add('is-invalid');
            let err = field.parentElement.querySelector('.form-error');
            if (!err) {
                err = document.createElement('div');
                err.className = 'form-error';
                field.parentElement.appendChild(err);
            }
            err.textContent = msg;
        },

        clearError(field) {
            field.classList.remove('is-invalid');
            const err = field.parentElement.querySelector('.form-error');
            if (err) err.textContent = '';
        },

        showErrors(form) {
            const first = form.querySelector('.is-invalid');
            if (first) first.focus();
        },
    };

    window.JobBridge = window.JobBridge || {};
    window.JobBridge.validation = validation;
})(window, document);