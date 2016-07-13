
Ext.define("CmsConfigExplorer.view.service.ServiceParameters",{
    extend: "Ext.tree.Panel",

    requires:['CmsConfigExplorer.view.service.ServiceParametersController'],
    
    controller: "service-serviceparameters",

    alias: 'widget.serviceparamstree',
    reference: "srvParamsTree",
    
    listeners:{
        cusTooltipActivate: 'onTooltipActivate',
        scope: 'controller'
    },
    
    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 1,
        listeners: {
            beforeedit: 'onBeforeCellEdit'  
        }
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{srvparams}'
//        selection: '{selectedModuleitem}'
    },
    bufferedRenderer: false,
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'rendervalue', flex: 1
        ,editor: {
                xtype: 'textfield',
                editable : false
            }
        },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer: function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'isDefault'}
//         'default', renderer: function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"} else {return "False"} }}
    ]
});
