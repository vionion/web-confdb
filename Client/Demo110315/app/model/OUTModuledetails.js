Ext.define('Demo110315.model.OUTModuledetails', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'mt', type: 'string' },
        { name: 'mclass', type: 'string' },
        { name: 'author', type: 'string' },
        { name: 'stream', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : '/outmoddetails',
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
