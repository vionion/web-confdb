
Ext.define("CmsConfigExplorer.view.streamdataset.EventContent",{
    extend: "Ext.grid.Panel",
    
    requires:['CmsConfigExplorer.view.streamdataset.EventContentController'],
    
    controller: "streamdataset-eventcontent",
    
    alias: 'widget.eventcontent',
    
    reference: "eventContentGrid",
    
    bind:{
        store:'{ecstats}'
    },

    scrollable: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        dock: 'top',
        
                    items:[ 
                    {
                        text: 'Keep',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop',
                        disabled: true
//                        listeners: {
//                            click: 'onDropClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Keep All',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepAllClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop All',
                        disabled: true
//                        listeners: {
//                            click: 'onDropAllClick',
//                            scope: 'controller'
//                        }
                    }
            ] 
    
    }],
    
    columns:[
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'stype', flex: 1 },
        { xtype: 'gridcolumn', header: 'Class Name', dataIndex: 'classn', flex: 1 },
        { xtype: 'gridcolumn', header: 'Module element', dataIndex: 'modulel', flex: 1 },
        { xtype: 'gridcolumn', header: 'Extra name', dataIndex: 'extran', flex: 1 },
        { xtype: 'gridcolumn', header: 'Process name', dataIndex: 'processn', flex: 1 }
    ]
    
});
