Ext.define('CmsConfigExplorer.model.Summaryitem', {
    extend: 'CmsConfigExplorer.model.Base',
    
    fields: [
        { name: 'name', type: 'string' },
        { name: 'sit', type: 'string' }
//        ,{ name: 'order', type: 'int'}

    ],
    
    proxy: {
        type: 'ajax',
        url : 'allsummaryitems',
        timeout : 240000,
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
