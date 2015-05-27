
Ext.define("Demo110315.view.sequence.Parameters",{
    extend: "Ext.tree.Panel",

    controller: "sequence-parameters",

    alias:'widget.seqparameters',
    
    reference: "seqParamGrid",
bind:{
        // bind store to view model "modules" store
        store:'{seqparameters}'
//        selection: '{selectedModuleitem}'
    },
    
    title: 'Parameters',
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
//        { xtype: 'gridcolumn', header: 'ORD', dataIndex: 'order' },
//        { xtype: 'gridcolumn', header: 'LVL', dataIndex: 'lvl' },
//        { xtype: 'gridcolumn', header: 'id', dataIndex: 'gid' },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'value' },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer:function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "Tracked"} else {return "Untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
