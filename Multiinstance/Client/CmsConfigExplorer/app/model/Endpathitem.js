Ext.define('CmsConfigExplorer.model.Endpathitem', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'Name', type: 'string' },
        { name: 'pit', type: 'string' },
        { name: 'vid', type: 'int' , defaultValue: -1},
        { name: 'order', type: 'int'}

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allendpathitems',
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
