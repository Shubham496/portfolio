// ─────────────────────────────────────────────
// Theme toggle (dark / light)
// ─────────────────────────────────────────────
document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon        = document.getElementById('theme-toggle-sun-icon');
    const moonIcon       = document.getElementById('theme-toggle-moon-icon');

    function updateThemeUI() {
        const isDark = document.documentElement.classList.contains('dark');
        moonIcon.classList.toggle('hidden', !isDark);
        sunIcon.classList.toggle('hidden', isDark);
    }
    if (themeToggleBtn) {
        updateThemeUI();
        themeToggleBtn.addEventListener('click', () => {
            const isDark = document.documentElement.classList.contains('dark');
            document.documentElement.classList.toggle('dark', !isDark);
            localStorage.setItem('color-theme', isDark ? 'light' : 'dark');
            updateThemeUI();
        });
    }

    // Mobile menu toggle
    const mobileBtn  = document.getElementById('mobile-menu-btn');
    const mobileMenu = document.getElementById('mobile-menu');
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('hidden');
        });
        // Close mobile menu on nav link click
        mobileMenu.querySelectorAll('a').forEach(a => {
            a.addEventListener('click', () => mobileMenu.classList.add('hidden'));
        });
    }

    // Wire up forms
    bindForm('enroll-form',  '/api/courses/register', 'enroll-submit-btn',
        '🎉 Registered!',
        'Your seat is reserved. Shubham will confirm your batch details shortly.');

    bindForm('enquiry-form', '/api/courses/enquiry',  'enquiry-submit-btn',
        '✅ Enquiry Sent!',
        'Got your message! Shubham will get back to you very soon.');

    // ESC key closes modals
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeAllModals();
    });
});


// ─────────────────────────────────────────────
// Modal open / close
// ─────────────────────────────────────────────
function openModal(which) {
    const backdrop = document.getElementById('modal-backdrop');
    const modal    = document.getElementById('modal-' + which);
    if (!backdrop || !modal) return;

    // Close any other open modal first
    closeAllModals(false);

    backdrop.classList.remove('hidden');
    modal.classList.remove('hidden');

    // Focus first input
    const firstInput = modal.querySelector('input, textarea, select');
    if (firstInput) setTimeout(() => firstInput.focus(), 50);

    // Prevent body scroll
    document.body.style.overflow = 'hidden';
}

function closeAllModals(restoreScroll = true) {
    document.getElementById('modal-backdrop')?.classList.add('hidden');
    document.getElementById('modal-enroll')?.classList.add('hidden');
    document.getElementById('modal-enquiry')?.classList.add('hidden');
    if (restoreScroll) document.body.style.overflow = '';
}


// ─────────────────────────────────────────────
// Form submission (Fetch → JSON → toast)
// ─────────────────────────────────────────────
function bindForm(formId, endpoint, submitBtnId, successTitle, successMsg) {
    const form      = document.getElementById(formId);
    const submitBtn = document.getElementById(submitBtnId);
    if (!form) return;

    form.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Build JSON payload from form
        const data = {};
        new FormData(form).forEach((val, key) => { data[key] = val; });

        // Loading state
        submitBtn.disabled = true;
        const originalHTML = submitBtn.innerHTML;
        submitBtn.innerHTML = `<svg class="w-4 h-4 animate-spin mr-2" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg><span>Sending…</span>`;

        try {
            const res = await fetch(endpoint, {
                method:  'POST',
                headers: { 'Content-Type': 'application/json' },
                body:    JSON.stringify(data)
            });

            if (res.ok || res.status === 201) {
                closeAllModals();
                form.reset();
                showToast('success', successTitle, successMsg);
            } else {
                const err = await res.json().catch(() => ({}));
                const detail = Array.isArray(err.detail)
                    ? err.detail.map(d => d.msg).join(', ')
                    : (err.detail || 'Something went wrong. Please try again.');
                showToast('error', 'Submission Failed', detail);
            }
        } catch (_) {
            showToast('error', 'Network Error', 'Unable to reach the server. Please check your connection.');
        } finally {
            submitBtn.disabled = false;
            submitBtn.innerHTML = originalHTML;
            // Re-create lucide icons for the restored button HTML
            if (typeof lucide !== 'undefined') lucide.createIcons();
        }
    });
}


// ─────────────────────────────────────────────
// Toast
// ─────────────────────────────────────────────
let toastTimer = null;

function showToast(type, title, message) {
    const toast      = document.getElementById('toast');
    const inner      = document.getElementById('toast-inner');
    const iconEl     = document.getElementById('toast-icon');
    const titleEl    = document.getElementById('toast-title');
    const msgEl      = document.getElementById('toast-msg');
    if (!toast) return;

    titleEl.textContent = title;
    msgEl.textContent   = message;

    // Reset classes
    inner.className = 'flex items-start space-x-3 px-4 py-3.5 rounded-xl shadow-2xl border text-sm font-medium transition-all';
    iconEl.className = 'w-5 h-5 mt-0.5 shrink-0';

    if (type === 'success') {
        inner.classList.add('bg-emerald-50', 'dark:bg-emerald-950', 'border-emerald-200', 'dark:border-emerald-800', 'text-emerald-900', 'dark:text-emerald-100');
        iconEl.setAttribute('data-lucide', 'circle-check-big');
        iconEl.classList.add('text-emerald-600');
    } else {
        inner.classList.add('bg-red-50', 'dark:bg-red-950', 'border-red-200', 'dark:border-red-800', 'text-red-900', 'dark:text-red-100');
        iconEl.setAttribute('data-lucide', 'circle-x');
        iconEl.classList.add('text-red-600');
    }

    if (typeof lucide !== 'undefined') lucide.createIcons();

    toast.classList.remove('hidden');

    if (toastTimer) clearTimeout(toastTimer);
    toastTimer = setTimeout(() => toast.classList.add('hidden'), 5000);
}
