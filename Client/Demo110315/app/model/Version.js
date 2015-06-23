Ext.define('Demo110315.model.Version', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'created', type: 'string' },
        { name: 'creator', type: 'string' },
        { name: 'ver', type: 'int' },
        { name: 'description', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : '/versions',
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
