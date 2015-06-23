
Ext.define("Demo110315.view.explorer.Folders",{
    extend: "Ext.tree.Panel",

    requires:['Demo110315.model.Folderitem',
             'Demo110315.model.Version'],
    
    alias: "widget.folders",
    
    reference: 'foldersTree',
    
    controller: "explorer-folders",

    bind:{
        // bind store to view model "modules" store
        store:'{folderitems}',
        selection: '{selectedFolderitem}'
    },
    
    title: "Folder Explorer",
    loadMask: true,
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'new_name', flex: 1 }
//        { xtype: 'gridcolumn', header: 'id', dataIndex: 'gid' },
//        { xtype: 'gridcolumn', header: 'fit', dataIndex: 'fit' }
    ],
    
    listeners: {
        rowclick: 'onConfClick',
        rowdblclick:  'onConfDblClick',
        scope: 'controller'    
    }
    
});
