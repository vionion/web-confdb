
Ext.define("Demo110315.view.service.ServiceGrid",{
    extend: "Ext.tree.Panel",
    
    alias: 'widget.servicesgrid',
    reference: 'servicesGrid',
    
    controller: "service-servicegrid",

//    listeners: {
//        rowclick: 'onGridServiceClick',
//        scope: 'controller'    
//    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{services}',
        selection: '{selectedService}'
 
    },
    
    title: 'Configuration Services',
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
