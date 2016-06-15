
Ext.define("CmsConfigExplorer.view.sequence.Parameters",{
    extend: "Ext.tree.Panel",

    controller: "sequence-parameters",

    alias:'widget.seqparameters',
    
    reference: "seqParamGrid",
bind:{
        // bind store to view model "modules" store
        store:'{seqparameters}'
//        selection: '{selectedModuleitem}'
    },
    
    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 1,
        listeners: {
            beforeedit: 'onBeforeCellEdit'  
        }
    },
    
    bufferedRenderer: false,
    
    title: 'Parameters',
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'rendervalue'
        ,editor: {
                xtype: 'textfield',
                editable : false
            }
        },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer:function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "Tracked"} else {return "Untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'isDefault'}
//         'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
