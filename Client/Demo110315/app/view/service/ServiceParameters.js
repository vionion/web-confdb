
Ext.define("Demo110315.view.service.ServiceParameters",{
    extend: "Ext.tree.Panel",

    controller: "service-serviceparameters",

    alias: 'widget.serviceparamstree',
    reference: "srvParamsTree",

    bind:{
        // bind store to view model "modules" store
        store:'{srvparams}'
//        selection: '{selectedModuleitem}'
    },
    
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
//        { xtype: 'gridcolumn', header: 'ORD', dataIndex: 'order' },
//        { xtype: 'gridcolumn', header: 'LVL', dataIndex: 'lvl' },
//        { xtype: 'gridcolumn', header: 'id', dataIndex: 'gid' },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'value', flex: 1},
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer: function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'default', renderer: function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"} else {return "False"} }}
    ]
});
