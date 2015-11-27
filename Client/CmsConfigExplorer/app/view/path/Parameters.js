
Ext.define("CmsConfigExplorer.view.path.Parameters",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.path.ParametersController'],
    
    alias:'widget.parameters',
    
    reference: "paramGrid",
    
    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 1,
        listeners: {
            beforeedit: 'onBeforeCellEdit'  
        }
    },
    
    controller: "path-parameters",

    listeners:{
        cusTooltipActivate: 'onTooltipActivate',
        scope: 'controller'
    },
//    
    bind:{
        // bind store to view model "modules" store
        store:'{parameters}'
//        selection: '{selectedModuleitem}'
    },
    
    title: 'Parameters',
    rootVisible: true,
    useArrows: true,
    bufferedRenderer: false,
    enableQuickTips: true,
    loadMask: true,
    
    columns: [
        {
         xtype: 'treecolumn', 
         header: 'Name', 
         dataIndex: 'name', 
         flex: 1
        ,editor: {
            xtype: 'textfield',
            editable : false
            }
        },

//        { xtype: 'gridcolumn', 
//         header: 'Value', 
//         dataIndex: 'rendervalue', 
//         flex: 1
//        },
        
        { xtype: 'gridcolumn', 
         header: 'Value', 
         dataIndex: 'rendervalue', 
         flex: 1,
         editor: {
                xtype: 'textarea',
                editable : false

            }
        },
        
//        { xtype: 'widgetcolumn', 
//         header: 'Value', 
//         dataIndex: 'rendervalue', 
//         flex: 1,
//         widget: {
//                xtype: 'cellvaluexpand',
//                textTpl: 'rendervalue'
//            }
//        },
        
        
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer:function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'isDefault'}
//         'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
