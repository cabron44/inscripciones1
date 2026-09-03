document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const html = document.documentElement;
    const icon = themeToggle ? themeToggle.querySelector('i') : null;
    const savedTheme = localStorage.getItem('theme') || 'light';

    const updateThemeIcon = (isDark) => {
        if (!icon) {
            return;
        }

        icon.classList.toggle('fa-adjust', !isDark);
        icon.classList.toggle('fa-sun', isDark);
    };

    if (savedTheme === 'dark') {
        html.setAttribute('data-bs-theme', 'dark');
        updateThemeIcon(true);
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = html.getAttribute('data-bs-theme') === 'dark';

            if (isDark) {
                html.removeAttribute('data-bs-theme');
                localStorage.setItem('theme', 'light');
            } else {
                html.setAttribute('data-bs-theme', 'dark');
                localStorage.setItem('theme', 'dark');
            }

            updateThemeIcon(!isDark);
        });
    }
});
