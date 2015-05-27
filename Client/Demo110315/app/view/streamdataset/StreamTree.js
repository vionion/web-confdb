
Ext.define("Demo110315.view.streamdataset.StreamTree",{
    extend: "Ext.tree.Panel",

    alias: 'widget.streamtree',
    
    controller: "streamdataset-streamtree",

    reference: "streamTree",
    
    bind:{
        store:'{streamitems}'
    },
    
    title: "Stream and Datasets",
    rootVisible: true,
    useArrows: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 }

    ]
});
