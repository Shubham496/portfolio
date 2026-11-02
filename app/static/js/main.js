// Theme toggle functionality (Dark / Light)
document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById('theme-toggle');
    const sunIcon = document.getElementById('theme-toggle-sun-icon');
    const moonIcon = document.getElementById('theme-toggle-moon-icon');

    if (!themeToggleBtn || !sunIcon || !moonIcon) return;

    // Show Sun icon in Light mode, Moon icon in Dark mode
    function updateThemeUI() {
        const isDark = document.documentElement.classList.contains('dark');
        if (isDark) {
            moonIcon.classList.remove('hidden');
            sunIcon.classList.add('hidden');
        } else {
            sunIcon.classList.remove('hidden');
            moonIcon.classList.add('hidden');
        }
    }

    // Set initial icon correctly on page load
    updateThemeUI();

    themeToggleBtn.addEventListener('click', () => {
        const isDark = document.documentElement.classList.contains('dark');
        if (isDark) {
            document.documentElement.classList.remove('dark');
            localStorage.setItem('color-theme', 'light');
        } else {
            document.documentElement.classList.add('dark');
            localStorage.setItem('color-theme', 'dark');
        }
        updateThemeUI();
    });
});
