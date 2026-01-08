// Скрывает/показывает содержимое под спойлером

const spoilerToggles = document.querySelectorAll('.spoiler-toggle');

spoilerToggles.forEach(button => {
    button.addEventListener('click', () => {
        const spoiler = button.closest('.spoiler');
        if (spoiler) {
            spoiler.classList.toggle('is-open');
        }
    });
});