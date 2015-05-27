
Ext.define("Demo110315.view.streamdataset.EventContent",{
    extend: "Ext.grid.Panel",

    controller: "streamdataset-eventcontent",
    
    alias: 'widget.eventcontent',
    
    reference: "eventContentGrid",
    
    bind:{
        store:'{ecstats}'
    },

    scrollable: true, 
    columns:[
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'stype', flex: 1 },
        { xtype: 'gridcolumn', header: 'Class Name', dataIndex: 'classn', flex: 1 },
        { xtype: 'gridcolumn', header: 'Module element', dataIndex: 'modulel', flex: 1 },
        { xtype: 'gridcolumn', header: 'Extra name', dataIndex: 'extran', flex: 1 },
        { xtype: 'gridcolumn', header: 'Process name', dataIndex: 'processn', flex: 1 }
    ]
    
});
