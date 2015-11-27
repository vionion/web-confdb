Ext.define('CmsConfigExplorer.model.Folderitem', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'new_name', type: 'string' },
        { name: 'fit', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'directories',
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
    }
});
