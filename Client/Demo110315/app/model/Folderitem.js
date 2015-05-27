Ext.define('Demo110315.model.Folderitem', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'new_name', type: 'string' },
        { name: 'fit', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : '/directories',
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
