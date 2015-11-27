
Ext.define("CmsConfigExplorer.view.explorer.Folders",{
    extend: "Ext.tree.Panel",

    requires:['CmsConfigExplorer.model.Folderitem',
             'CmsConfigExplorer.model.Version'],
    
    alias: "widget.folders",
    
    reference: 'foldersTree',
    
    controller: "explorer-folders",

    bind:{
        store:'{folderitems}',
        selection: '{selectedFolderitem}'
    },
    
    title: "Folder Explorer",
    loadMask: true,
//    rootVisible: true,
    useArrows: true,
//    folderSort:true,
    
    columns: [
        { xtype: 'treecolumn', header: 'Name', dataIndex: 'new_name', flex: 1 }
    ],
    
    listeners: {
        rowclick: 'onConfClick',
        rowdblclick:  'onConfDblClick',
        scope: 'controller'    
    }
    
});
