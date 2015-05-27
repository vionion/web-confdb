Ext.define('Demo110315.model.Streamitem', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'fracktodisk', type: 'int' },
        { name: 's_type', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : '/allstreamitems',
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
