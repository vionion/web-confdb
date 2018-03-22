Ext.define('CmsConfigExplorer.model.InputTag', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'name', type: 'string'}
    ],

    proxy: {
        type: 'ajax',
        url: 'allmodules',
        limitParam: '',
        pageParam: '',
        sortParam: '',
        startParam: '',
        headers: {'Content-Type': "application/json"},
        reader: {
            type: 'json',
            rootProperty: 'children'
        }
    }
});