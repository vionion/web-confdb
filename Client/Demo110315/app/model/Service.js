Ext.define('Demo110315.model.Service', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'stype', type: 'string' },
        { name: 'vid', type: 'int' , defaultValue: -1}

    ],
    
    proxy: {
        type: 'ajax',
        url : '/allservices',
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
