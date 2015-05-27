
Ext.define("Demo110315.view.streamdataset.PathsTree",{
    extend: "Ext.tree.Panel",

    controller: "streamdataset-pathstree",
    
    alias: 'widget.datasetpaths',
    
    reference: "datasetPathsTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{datasetpaths}'

    },
    header: false,
//    title: "Paths",
    rootVisible: true,
    useArrows: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 }

    ]
});
