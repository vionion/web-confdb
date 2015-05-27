
Ext.define("Demo110315.view.edsource.EDSourceGrid",{
    extend: "Ext.tree.Panel",

    controller: "edsource-edsourcegrid",

    alias: 'widget.edsourcegrid',

    listeners: {
        rowclick: 'onGridEDSourceClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{edsource}'
//        ,selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridEDSourceClick',
        scope: 'controller'    
    },
    loadMask: true,
    
    reference: 'edSourceGrid',
    
    title: 'Configuration ED Source',
    
    useArrows: true,
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        }

    ]
});
