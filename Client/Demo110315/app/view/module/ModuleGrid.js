
Ext.define("Demo110315.view.module.ModuleGrid",{
    extend: "Ext.grid.Panel",

    controller: "module-modulegrid",
    
    alias: 'widget.modulesgrid',

    listeners: {
        rowclick: 'onGridModuleClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{modules}',
        selection: '{selectedModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridModuleClick',
        scope: 'controller'    
    },
    loadMask: true,
    viewConfig: {
        loadingHeight: 100
    },
    reference: 'modulesGrid',
    
    title: 'Configuration Modules',
    
    columns: [
        {
            xtype: 'gridcolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
//        {
//            xtype: 'gridcolumn',
//            text: 'ID',
//            flex: 1,
//            dataIndex: 'gid'
//
//        },
        {
            xtype: 'gridcolumn',
            text: 'Class',
            flex: 1,
            dataIndex: 'mclass'

        },
        {
            xtype: 'gridcolumn',
            text: 'Type',
            flex: 1,
            dataIndex: 'mt'

        }
    ]
});
