document.addEventListener('DOMContentLoaded', function() {
    
    // --- Логика для десктопного поиска ---
    const desktopSearchButton = document.getElementById('searchBtn');
    const desktopSearchInput = document.getElementById('searchInput');

    if (desktopSearchButton) {
        desktopSearchButton.addEventListener('click', function(event) {
            event.stopPropagation();
            desktopSearchInput.classList.toggle('active');
            if (desktopSearchInput.classList.contains('active')) {
                desktopSearchInput.focus();
            }
        });
    }

    document.addEventListener('click', function(event) {
        if (desktopSearchInput && desktopSearchInput.classList.contains('active')) {
            const isClickInside = desktopSearchInput.contains(event.target) || desktopSearchButton.contains(event.target);
            if (!isClickInside) {
                desktopSearchInput.classList.remove('active');
            }
        }
    });

    // --- Логика для мобильного меню и поиска ---
    const hamburgerBtn = document.getElementById('hamburgerBtn');
    const sidebarNav = document.getElementById('sidebarNav');
    const closeMenuBtn = document.getElementById('closeMenuBtn');
    const overlay = document.getElementById('overlay');
    
    const mobileSearchToggle = document.getElementById('mobileSearchToggle');
    const mobileSearchContainer = document.getElementById('mobileSearchContainer');

    // Открытие/закрытие бургер-меню
    if (hamburgerBtn) {
        hamburgerBtn.addEventListener('click', () => {
            sidebarNav.classList.add('show');
            overlay.classList.add('show');
            document.body.classList.add('menu-open'); // Блокируем скролл страницы
        });
    }

    const closeMenu = () => {
        sidebarNav.classList.remove('show');
        overlay.classList.remove('show');
        document.body.classList.remove('menu-open');
    };

    if (closeMenuBtn) {
        closeMenuBtn.addEventListener('click', closeMenu);
    }
    if (overlay) {
        overlay.addEventListener('click', closeMenu);
    }

    // Открытие/закрытие мобильного поиска
    if (mobileSearchToggle) {
        mobileSearchToggle.addEventListener('click', () => {
            mobileSearchContainer.classList.toggle('active');
            mobileSearchToggle.classList.toggle('active');
            
            // Если поиск открыли, ставим фокус в поле ввода
            if (mobileSearchContainer.classList.contains('active')) {
                mobileSearchContainer.querySelector('input').focus();
            }
        });
    }
});3

// --- Логика для интерактивного содержания (TOC) ---
const tocHeaders = document.querySelectorAll('.toc-category-header');

tocHeaders.forEach(header => {
    header.addEventListener('click', () => {
        // Находим родительский элемент категории
        const category = header.closest('.toc-category');
        // Находим кнопку внутри шапки, чтобы менять ее текст
        const button = header.querySelector('.toc-toggle-btn');
        
        if (category && button) {
            category.classList.toggle('is-open');
            if (category.classList.contains('is-open')) {
                button.textContent = '-';
            } else {
                button.textContent = '+';
            }
        }
    });
});

// --- Логика для спойлера ---
const spoilerToggles = document.querySelectorAll('.spoiler-toggle');

spoilerToggles.forEach(button => {
    button.addEventListener('click', () => {
        const spoiler = button.closest('.spoiler');
        if (spoiler) {
            spoiler.classList.toggle('is-open');
        }
    });
});

// --- Логика для кнопки "Поделиться" ---
const shareBlock = document.getElementById('shareBlock');
const shareToggleBtn = document.getElementById('shareToggleBtn');

if (shareToggleBtn) {
    shareToggleBtn.addEventListener('click', function(event) {
        // Предотвращаем "всплытие", чтобы клик по кнопке не закрыл меню сразу же
        event.stopPropagation();
        shareBlock.classList.toggle('is-active');
    });
}

// Закрываем меню, если клик был в любом другом месте на странице
document.addEventListener('click', function(event) {
    if (shareBlock && shareBlock.classList.contains('is-active')) {
        // Проверяем, был ли клик вне блока "Поделиться"
        if (!shareBlock.contains(event.target)) {
            shareBlock.classList.remove('is-active');
        }
    }
});