Ext.define('CmsConfigExplorer.model.EDSourceitem', {
    extend: 'Ext.data.Model',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'mit', type: 'string' },
        { name: 'value', type: 'string' },
        { name: 'tracked', type: 'int' },
//        { name: 'default', type: 'int' },
        { name: 'isDefault', type: 'string' },
        { name: 'paramtype', type: 'string' }

    ],
    
    proxy: {
        type: 'ajax',
        url : 'alledsourceitems',
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
