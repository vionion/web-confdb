
Ext.define("Demo110315.view.esmodule.ESModuleGrid",{
    extend: "Ext.tree.Panel",

    controller: "esmodule-esmodulegrid",

    alias: 'widget.esmodulesgrid',

    listeners: {
        rowclick: 'onGridESModuleClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{esmodules}',
        selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridESModuleClick',
        scope: 'controller'    
    },
    loadMask: true,
    
    reference: 'esModulesGrid',
    
    title: 'Configuration ES Modules',
    
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
            flex: 1,
            dataIndex: 'mclass'

        }
    ]
});
