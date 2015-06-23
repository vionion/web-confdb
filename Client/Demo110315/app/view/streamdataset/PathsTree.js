
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
    rootVisible: false,
    useArrows: true,
    scrollable: true,
    bufferedRenderer: false,
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 , sortable: true}

    ]
});
