
Ext.define("CmsConfigExplorer.view.param.Parameters",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.param.ParametersController'],
    
    alias:'widget.parameters',
    
    reference: "paramGrid",
    
    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 2,
        listeners: {
            beforeedit: 'onBeforeCellEdit',
            edit: 'onEditDone'
        }
    },
    
    controller: "parameters",

    listeners:{
        cusTooltipActivate: 'onTooltipActivate',
        scope: 'controller'
    },
//    
    bind: {
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
            flex: 1,
            editor: {
                xtype: 'textfield',
                editable: false
            }
        },
        {
            xtype: 'gridcolumn',
            header: 'Value',
            dataIndex: 'rendervalue',
            flex: 1,
            editor: {
                xtype: 'textarea',
                editable: true
            },
            renderer: function (v, meta, rec) {
                var data = rec.getData();
                if ((data.paramtype === 'InputTag') && v && (inputTags.findExact('name', v.split(":")[0]) === -1)) {
                    meta.style = "color:red;";
                }
                return v;
            }
        },
        {
            xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked', renderer: function (v, meta, rec) {
                var data = rec.getData();
                if (data.tracked == 1) {
                    return "tracked"
                } else {
                    return "untracked"
                }
            }
        },
        {xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype'},
        {xtype: 'gridcolumn', header: 'Default', dataIndex: 'isDefault'}
//         'default', renderer:function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"}else{return "False"} }}
    ]
});
