
Ext.define("CmsConfigExplorer.view.endpath.EndPathParameters",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.endpath.EndPathParametersController'],
    
    alias:'widget.endparameters',
    
    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 1,
        listeners: {
            beforeedit: 'onBeforeCellEdit'  
        }
    },
    
    reference: "endParamGrid",
    
    controller: "endpath-endpathparameters",
    
    listeners:{
        cusTooltipActivate: 'onTooltipActivate',
        scope: 'controller'
    },
    
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
//        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'rendervalue' },
        { xtype: 'gridcolumn', 
         header: 'Value', 
         dataIndex: 'rendervalue', 
         flex: 1
         ,editor: {
                xtype: 'textfield',
                editable : false
            }
        },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer:function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'isDefault'}
//         'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
