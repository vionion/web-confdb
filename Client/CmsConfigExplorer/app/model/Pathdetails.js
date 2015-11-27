Ext.define('CmsConfigExplorer.model.Pathdetails', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'labels', type: 'auto' },
        { name: 'values', type: 'auto' },
        { name: 'author', type: 'string' },
        { name: 'desc', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'pathdetails',
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
