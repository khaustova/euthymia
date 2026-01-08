CKEDITOR.plugins.add('spoiler', {
    lang: 'ru,en',
    icons: 'spoiler',
    init: function(editor) {
        
        editor.addCommand('spoiler', {
            exec: function(editor) {
                // Главный контейнер
                var spoilerContainer = editor.document.createElement('div', {
                    'attributes': { 'class': 'spoiler' }
                });

                // Кнопка
                var spoilerToggle = editor.document.createElement('button', {
                    'attributes': { 'class': 'spoiler-toggle' }
                });
                var icon = editor.document.createElement('i', {
                    'attributes': { 'class': 'fas fa-plus' }
                });
                spoilerToggle.append(icon);
                spoilerToggle.appendText(' Ответ');

                // Внешний контейнер для анимации
                var spoilerContent = editor.document.createElement('div', {
                    'attributes': { 'class': 'spoiler-content' }
                });
                
                // Внутренний контейнер для отступов
                var spoilerInner = editor.document.createElement('div', {
                    'attributes': { 'class': 'spoiler-inner' }
                });

                // Добавляем параграф по умолчанию внутрь .spoiler-inner
                spoilerInner.appendHtml('<p>Введите текст спойлера здесь...</p>');
                
                // Вкладываем внутренний блок во внешний
                spoilerContent.append(spoilerInner);

                // Собираем все элементы вместе
                spoilerContainer.append(spoilerToggle);
                spoilerContainer.append(spoilerContent);

                editor.insertElement(spoilerContainer);
            },
            // Разрешаем новый класс .spoiler-inner
            allowedContent: 'div(spoiler,spoiler-content,spoiler-inner); button(spoiler-toggle); p'
        });

        editor.ui.addButton('Spoiler', {
            label: 'Вставить спойлер',
            command: 'spoiler',
            toolbar: 'insert'
        });
    }
});