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
        'Your seat is reserved. Our admissions desk will confirm your batch schedule shortly.');

    bindForm('enquiry-form', '/api/courses/enquiry',  'enquiry-submit-btn',
        '✅ Enquiry Sent!',
        'Got your message! Our admissions advisor will get back to you shortly.');

    bindForm('waitlist-form', '/api/courses/waitlist', 'waitlist-submit-btn',
        '🚀 On the Waitlist!',
        'You are on the priority waitlist! We will notify you via WhatsApp as soon as enrollment opens.');

    bindForm('demo-form', '/api/courses/demo', 'demo-submit-btn',
        '🎉 Demo Reservation Confirmed!',
        'Your seat for the free live demo class is reserved! We will send the meeting link to your WhatsApp.');

    // Lead Magnet Form AJAX Handler
    const lmForm = document.getElementById('lead-magnet-form');
    if (lmForm) {
        lmForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const submitBtn = document.getElementById('lead-magnet-submit-btn');
            const data = {};
            new FormData(lmForm).forEach((val, key) => { data[key] = val; });
            if (!data.source_utm) {
                const cookieMatch = document.cookie.match(/mythos_utm=([^;]+)/);
                if (cookieMatch) data.source_utm = decodeURIComponent(cookieMatch[1]);
            }
            if (!data.referrer_url && document.referrer) {
                data.referrer_url = document.referrer;
            }
            if (submitBtn) submitBtn.disabled = true;
            try {
                const res = await fetch('/api/courses/lead-magnet', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(data)
                });
                if (res.ok || res.status === 201) {
                    const result = await res.json();
                    const revealDiv = document.getElementById('lead-magnet-download-reveal');
                    const directBtn = document.getElementById('lead-magnet-direct-btn');
                    if (revealDiv && directBtn && result.download_url) {
                        directBtn.href = result.download_url;
                        revealDiv.classList.remove('hidden');
                        if (submitBtn) submitBtn.classList.add('hidden');
                    }
                    showToast('success', '🎉 Download Ready!', 'Your learning asset is ready. Click the download button below.');
                } else {
                    const err = await res.json().catch(() => ({}));
                    const detail = Array.isArray(err.detail) ? err.detail.map(d => d.msg).join(', ') : (err.detail || 'Submission failed.');
                    showToast('error', 'Download Failed', detail);
                    if (submitBtn) submitBtn.disabled = false;
                }
            } catch (_) {
                showToast('error', 'Network Error', 'Unable to reach the server.');
                if (submitBtn) submitBtn.disabled = false;
            }
        });
    }

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

function openModalWithCourse(which, courseName) {
    openModal(which);
    if (courseName) {
        const modal = document.getElementById('modal-' + which);
        if (modal) {
            const select = modal.querySelector('select[name="course_name"]') || modal.querySelector('select[name="course_interest"]');
            if (select) {
                for (let i = 0; i < select.options.length; i++) {
                    const opt = select.options[i];
                    if (opt.value === courseName || opt.text.includes(courseName) || courseName.includes(opt.value)) {
                        select.selectedIndex = i;
                        break;
                    }
                }
            }
        }
    }
}

function openWaitlistModal(subjectName) {
    openModal('waitlist');
    if (subjectName) {
        const input = document.getElementById('waitlist-subject-input');
        const badge = document.getElementById('waitlist-subject-badge');
        if (input) input.value = subjectName;
        if (badge) badge.textContent = subjectName;
    }
}

function openLeadMagnetModal(resourceName) {
    openModal('lead-magnet');
    if (resourceName) {
        const input = document.getElementById('lead-magnet-resource-input');
        const badge = document.getElementById('lead-magnet-resource-badge');
        if (input) input.value = resourceName;
        if (badge) badge.textContent = resourceName;
    }
}

function closeAllModals(restoreScroll = true) {
    document.getElementById('modal-backdrop')?.classList.add('hidden');
    document.getElementById('modal-enroll')?.classList.add('hidden');
    document.getElementById('modal-enquiry')?.classList.add('hidden');
    document.getElementById('modal-waitlist')?.classList.add('hidden');
    document.getElementById('modal-lead-magnet')?.classList.add('hidden');
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

        // Auto-attach UTM attribution tokens and referrer (Task 4.5)
        if (!data.source_utm) {
            const cookieMatch = document.cookie.match(/mythos_utm=([^;]+)/);
            if (cookieMatch) data.source_utm = decodeURIComponent(cookieMatch[1]);
        }
        if (!data.referrer_url && document.referrer) {
            data.referrer_url = document.referrer;
        }

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
                if (formId === 'enroll-form') {
                    window.location.href = '/registration-success';
                } else {
                    showToast('success', successTitle, successMsg);
                }
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


// ─────────────────────────────────────────────
// Expandable Syllabus Accordion
// ─────────────────────────────────────────────
function toggleSyllabus(index) {
    const content = document.getElementById(`syllabus-exp-${index}`);
    const btn = document.getElementById(`syllabus-btn-${index}`);
    const icon = document.getElementById(`syllabus-icon-${index}`);
    if (!content) return;

    const isClosed = content.classList.contains('hidden') || content.style.display === 'none' || window.getComputedStyle(content).display === 'none';
    if (isClosed) {
        content.classList.remove('hidden');
        content.style.display = 'block';
        if (btn) {
            const span = btn.querySelector('.btn-label') || btn.querySelector('span');
            if (span) span.textContent = 'Show Less Details';
        }
        if (icon) icon.style.transform = 'rotate(180deg)';
        if (window.lucide && typeof lucide.createIcons === 'function') {
            try { lucide.createIcons(); } catch (e) {}
        }
    } else {
        content.classList.add('hidden');
        content.style.display = 'none';
        if (btn) {
            const span = btn.querySelector('.btn-label') || btn.querySelector('span');
            if (span) span.textContent = 'Show More Details';
        }
        if (icon) icon.style.transform = 'rotate(0deg)';
    }
}

function toggleAllSyllabus() {
    const contents = document.querySelectorAll('.syllabus-expandable-content');
    const masterBtn = document.getElementById('toggle-all-syllabus-btn');
    if (!contents.length) return;

    // If any module is closed, expand all; otherwise collapse all
    let anyClosed = false;
    contents.forEach((c) => {
        if (c.classList.contains('hidden') || c.style.display === 'none' || window.getComputedStyle(c).display === 'none') {
            anyClosed = true;
        }
    });

    contents.forEach((c) => {
        const idx = c.id.replace('syllabus-exp-', '');
        const btn = document.getElementById(`syllabus-btn-${idx}`);
        const icon = document.getElementById(`syllabus-icon-${idx}`);
        if (anyClosed) {
            c.classList.remove('hidden');
            c.style.display = 'block';
            if (btn) {
                const s = btn.querySelector('.btn-label') || btn.querySelector('span');
                if (s) s.textContent = 'Show Less Details';
            }
            if (icon) icon.style.transform = 'rotate(180deg)';
        } else {
            c.classList.add('hidden');
            c.style.display = 'none';
            if (btn) {
                const s = btn.querySelector('.btn-label') || btn.querySelector('span');
                if (s) s.textContent = 'Show More Details';
            }
            if (icon) icon.style.transform = 'rotate(0deg)';
        }
    });

    if (masterBtn) {
        const masterSpan = masterBtn.querySelector('span');
        if (masterSpan) {
            masterSpan.textContent = anyClosed ? 'Collapse All Modules' : 'Expand All Modules';
        }
    }
    if (window.lucide && typeof lucide.createIcons === 'function') {
        try { lucide.createIcons(); } catch (e) {}
    }
}
