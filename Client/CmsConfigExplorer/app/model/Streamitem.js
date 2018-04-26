Ext.define('CmsConfigExplorer.model.Streamitem', {
    extend: 'Ext.data.Model',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'fracktodisk', type: 'int' },
        { name: 's_type', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allstreamitems',
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
