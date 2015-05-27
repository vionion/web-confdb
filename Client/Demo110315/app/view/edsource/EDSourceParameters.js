
Ext.define("Demo110315.view.edsource.EDSourceParameters",{
    extend: "Ext.tree.Panel",

    controller: "edsource-edsourceparameters",

    alias: 'widget.edsourceparamstree',
    reference: "edSourceParamsTree",
    
    requires:['Demo110315.model.EDSourceitem'],
    
    bind:{
        // bind store to view model "modules" store
        store:'{edsourceparams}'
//        selection: '{selectedModuleitem}'
    },
    
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Value', dataIndex: 'value' },
        { xtype: 'gridcolumn', header: 'Tracked', dataIndex: 'tracked',renderer: function(v, meta, rec) { var  data = rec.getData(); if (data.tracked == 1){return "tracked"} else {return "untracked"} }},
        { xtype: 'gridcolumn', header: 'Type', dataIndex: 'paramtype' },
        { xtype: 'gridcolumn', header: 'Default', dataIndex: 'default', renderer: function(v, meta, rec) {var  data = rec.getData(); if (data.default == 1){ return "True"} else {return "False"} }}
    ]
});
