Ext.define('CmsConfigExplorer.model.ESModule', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'class', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allesmodules',
        headers: {'Content-Type': "application/json" },
        limitParam: '',
        pageParam: '',
        sortParam: '',
        //extraParams: {'itype':'{selectedPathitem.pit}'},
        startParam : '',
        reader: {
            type: 'json',
            rootProperty: 'children'
        }
//        lazyFill: true
    }
});
