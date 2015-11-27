Ext.define('CmsConfigExplorer.model.Confname', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'url', type: 'string' }

    ],
    
     proxy: {
        type: 'ajax',
        url : 'confname',
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