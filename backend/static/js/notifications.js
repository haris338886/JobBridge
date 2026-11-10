/* ============================================================
   JobBridge — Toasts & flash messages
   ============================================================ */
(function (window, document) {
    'use strict';

    const notifications = {
        show(message, type = 'info', duration) {
            duration = duration || window.JobBridge.config.toastDuration;
            let container = document.querySelector('.messages-container');
            if (!container) {
                container = document.createElement('div');
                container.className = 'messages-container';
                document.body.appendChild(container);
            }
            const alert = document.createElement('div');
            alert.className = `alert alert-${type}`;
            alert.setAttribute('role', 'alert');
            alert.innerHTML = `<span>${message}</span>
                <button class="alert-close" aria-label="Dismiss">&times;</button>`;
            alert.querySelector('.alert-close').addEventListener('click', () => alert.remove());
            container.appendChild(alert);
            if (duration > 0) this.autoDismiss(alert, duration);
            return alert;
        },

        autoDismiss(alert, duration = 4000) {
            setTimeout(() => {
                alert.style.transition = 'opacity 0.3s, transform 0.3s';
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(20px)';
                setTimeout(() => alert.remove(), 300);
            }, duration);
        },
    };

    window.JobBridge = window.JobBridge || {};
    window.JobBridge.notifications = notifications;
})(window, document);