Ext.define('CmsConfigExplorer.model.Export', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'url', type: 'string' }

    ],
    
     proxy: {
        type: 'ajax',
        timeout : 240000,
        url : 'export',
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