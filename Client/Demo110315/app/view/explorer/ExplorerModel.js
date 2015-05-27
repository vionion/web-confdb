Ext.define('Demo110315.view.explorer.ExplorerModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.explorer-explorer',
    
    requires:['Demo110315.model.Folderitem',
             'Demo110315.model.Version'],
    
    data: {
        name: 'Demo110315'
    },
    
    stores:
    {        
        folderitems:{
            
            type:'tree', 
            model:'Demo110315.model.Folderitem', 
            autoLoad: false,

            root: {
                expanded: true,
                text: "Folders",
                gid: -1
            }
            
            ,listeners:{
                load: 'onFolderItemsLoad', 
                scope: 'controller'
            }
        },
        versions:{
                model:'Demo110315.model.Version',
                autoLoad:false
            }
    }

});
