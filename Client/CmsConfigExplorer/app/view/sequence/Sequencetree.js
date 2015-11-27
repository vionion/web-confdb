
Ext.define("CmsConfigExplorer.view.sequence.Sequencetree",{
    extend: "Ext.tree.Panel",

    controller: "sequence-sequencetree",

    alias: 'widget.seqtree',
    
    reference: "seqTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{seqitems}'
    },
    
    title: "Sequences",
    rootVisible: true,
    useArrows: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 }

    ]
});
