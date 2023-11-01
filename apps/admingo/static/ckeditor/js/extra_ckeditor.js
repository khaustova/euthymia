CKEDITOR.on('dialogDefinition', function (event) {
    try {
      var dialogName = event.data.name
      var dialogDefinition = event.data.definition

      if (dialogName === 'table' || dialogName === 'tableProperties') {
        var advancedTab = dialogDefinition.getContents('advanced')
        var infoTab = dialogDefinition.getContents('info')
        var txtWidth = infoTab.get('txtWidth')
        txtWidth.default = '100%'

        var stylesField = advancedTab.get('advStyles')
        stylesField.default = 'width: 100%;'

        var cssClassField = advancedTab.get('advCSSClasses')
        cssClassField.default = 'mod-table table-list-view' // 預設 class
      }
    } catch (exception) {
      window.alert('Error ' + event.message)
    }
  })

  CKEDITOR.on('instanceReady', function (event) {
    var editor = event.editor
  
    editor.on('change', function (e) {
      var tables = e.editor.document.$.querySelectorAll('table:not(.has-wrapper)')
      if (tables.length > 0) {
        tables.forEach(function (table) {
          table.classList.add('has-wrapper')
          $(table).wrap('<div class="mod-table-responsive"></div>')
        })
      }
    })
  })
  