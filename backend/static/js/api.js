/* ============================================================
   JobBridge — API client
   ============================================================ */
(function (window) {
    'use strict';

    const cfg = window.JobBridge.config;

    function getCsrfToken() {
        const name = 'csrftoken=';
        const parts = document.cookie.split(';').map(c => c.trim());
        const match = parts.find(p => p.startsWith(name));
        return match ? decodeURIComponent(match.substring(name.length)) : '';
    }

    async function request(url, options = {}) {
        const opts = {
            method: options.method || 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-Requested-With': 'XMLHttpRequest',
                ...(options.headers || {}),
            },
        };

        if (['POST', 'PUT', 'PATCH', 'DELETE'].includes(opts.method)) {
            opts.headers['X-CSRFToken'] = getCsrfToken();
        }
        if (options.body !== undefined) {
            opts.body = typeof options.body === 'string'
                ? options.body
                : JSON.stringify(options.body);
        }

        const res = await fetch(url, opts);
        const ct = res.headers.get('content-type') || '';
        const data = ct.includes('application/json') ? await res.json() : await res.text();

        if (!res.ok) {
            const err = new Error((data && data.detail) || `HTTP ${res.status}`);
            err.status = res.status;
            err.data = data;
            throw err;
        }
        return data;
    }

    window.JobBridge.api = {
        get(url)              { return request(url); },
        post(url, body)       { return request(url, { method: 'POST',   body }); },
        put(url, body)        { return request(url, { method: 'PUT',    body }); },
        patch(url, body)      { return request(url, { method: 'PATCH',  body }); },
        delete(url)           { return request(url, { method: 'DELETE' }); },

        jobs: {
            list(params = {}) { return request(cfg.endpoints.jobs + '?' + new URLSearchParams(params)); },
            get(id)           { return request(cfg.endpoints.jobs + id + '/'); },
            save(id)          { return request(cfg.endpoints.jobs + id + '/save/', { method: 'POST' }); },
        },
        applications: {
            create(body)      { return request(cfg.endpoints.applications, { method: 'POST', body }); },
            list(params = {}) { return request(cfg.endpoints.applications + '?' + new URLSearchParams(params)); },
        },
    };
})(window);