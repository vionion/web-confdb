Ext.define('Demo110315.model.Confdetails', {
    extend: 'Demo110315.model.Base',
    
    fields: [
        { name: 'name', type: 'string' }

    ],
    
     proxy: {
        type: 'ajax',
        url : '/cnfdetails',
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
