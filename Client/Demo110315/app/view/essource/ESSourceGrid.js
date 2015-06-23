
Ext.define("Demo110315.view.essource.ESSourceGrid",{
    extend: "Ext.tree.Panel",

    controller: "essource-essourcegrid",

    alias: 'widget.essourcegrid',

    listeners: {
        rowclick: 'onGridESSourceClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{essource}'
//        ,selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridESSourceClick',
        scope: 'controller'    
    },
    loadMask: true,
    
    reference: 'esSourceGrid',
    
    title: 'Configuration ES Source',
    useArrows: true,
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
        {
            xtype: 'gridcolumn',
            text: 'Class',
            flex: 2,
            dataIndex: 'tclass'
        }
    ]
});
