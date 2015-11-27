Ext.define('CmsConfigExplorer.model.Evcoitem', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
//        { name: 'name', type: 'string' },
        { name: 'stype', type: 'string' },
        { name: 'classn', type: 'string' },
        { name: 'modulel', type: 'string' },
        { name: 'extran', type: 'string' },
        { name: 'processn', type: 'string' }

    ],
    proxy: {
        type: 'ajax',
        url : 'evcostatements',
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
