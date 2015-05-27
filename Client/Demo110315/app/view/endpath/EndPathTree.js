
Ext.define("Demo110315.view.endpath.EndPathTree",{
    extend: "Ext.tree.Panel",

    alias: 'widget.endpathtree',
    
    controller: "endpath-endpathtree",

    reference: "endpathTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{endpathitems}'
    },
    
    title: "End Paths",
    rootVisible: true,
    useArrows: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 }
    ]
});
