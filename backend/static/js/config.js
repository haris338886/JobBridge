/* ============================================================
   JobBridge — Global config
   ============================================================ */
(function (window) {
    'use strict';

    window.JobBridge = window.JobBridge || {};

    window.JobBridge.config = {
        apiBase: '',
        endpoints: {
            jobs:          '/api/',
            applications:  '/applications/api/',
            companies:     '/companies/api/',
            candidates:    '/candidate/api/',
            notifications: '/notifications/api/',
            reviews:       '/reviews/api/',
            interviews:    '/interviews/api/',
            login:         '/accounts/api/login/',
            register:      '/accounts/api/register/',
            refresh:       '/accounts/api/token/refresh/',
        },
        pagination: { pageSize: 20 },
        toastDuration: 4000,
        debounceDelay: 250,
    };
})(window);