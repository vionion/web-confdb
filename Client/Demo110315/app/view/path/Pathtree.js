
Ext.define("Demo110315.view.path.Pathtree",{
    extend: "Ext.tree.Panel",
    
    alias: 'widget.pathtree',
    
    controller: "path-pathtree",
    
    reference: "pathTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{pathitems}'
//        selection: '{selectedPathitem}'
    },
    
    title: "Paths",
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1 }
//        { xtype: 'gridcolumn', header: 'id', dataIndex: 'gid' },
//        { xtype: 'gridcolumn', header: 'pit', dataIndex: 'pit' }
    ]
    
//    listeners: {
//        rowclick: 'onModuleClick',
//        scope: 'controller'    
//    }
});
