Ext.define('Demo110315.model.EDSourceitem', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'mit', type: 'string' },
        { name: 'value', type: 'string' },
        { name: 'tracked', type: 'int' },
        { name: 'default', type: 'int' },
        { name: 'paramtype', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : '/alledsourceitems',
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
