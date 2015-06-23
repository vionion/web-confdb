
Ext.define("Demo110315.view.endpath.EndPathParameters",{
    extend: "Ext.tree.Panel",

    alias:'widget.endparameters',
    
    reference: "endParamGrid",
    
    controller: "endpath-endpathparameters",

    bind:{
        // bind store to view model "modules" store
        store:'{endparameters}'
    },
    
    title: 'Parameters',
    rootVisible: true,
    useArrows: true,
    bufferedRenderer: false,
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'value' },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer:function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
