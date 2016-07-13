Ext.define('CmsConfigExplorer.view.path.PathModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-path',
    
    requires:['CmsConfigExplorer.model.Pathitem',
             'CmsConfigExplorer.model.Moduleitem',
             'CmsConfigExplorer.model.Moduledetails',
             'CmsConfigExplorer.model.Pathdetails'],
    
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        first: true,
        sortToogle: false,
        pathsLoaded: false,
        online: "False",
        modulesLoaded: false
    },
    
    stores:
    {        
        pathitems:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.Pathitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Paths",
                gid: -1
//                root: true
            },
            
            listeners: {

                load: 'onPathitemsLoad', 
                scope: 'controller',
                
                beforeload: 'onPathitemsBeforeLoad'
            }
        },
        parameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.Moduleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Params",
                    gid: -1
    //                root: true
                },
            
                listeners: {
                    
                    load: "onPathModuleParametersLoad"
                }
            
            }
    }

});
