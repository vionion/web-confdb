Ext.define('CmsConfigExplorer.view.explorer.ExplorerModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.explorer-explorer',
    
    requires:['CmsConfigExplorer.model.Folderitem',
             'CmsConfigExplorer.model.Version'],
    
    data: {
        name: 'CmsConfigExplorer',
        appversion: 'v1.2.2'
    },
    
    stores:
    {        
        folderitems:{
            
            type:'tree', 
            model:'CmsConfigExplorer.model.Folderitem', 
            autoLoad: false,

            root: {
                expanded: false,
                text: "Folders",
                new_name: "Folders",
                gid: -1
            }
            
            ,listeners:{
                
                beforeload: 'onFoldertemsBeforeLoad',
                load: 'onFolderItemsLoad', 
                scope: 'controller'
                           
            }
        },
        versions:{
                model:'CmsConfigExplorer.model.Version',
                autoLoad:false
            }
    }

});
