Ext.define('CmsConfigExplorer.view.esmodule.ESModuleModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.esmodule-esmodule',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        online: "False",
        first: true
    },
    
    requires:['CmsConfigExplorer.model.ESModule',
             'CmsConfigExplorer.model.ESModuleitem'],
    
    stores:
    {        
        esmodules:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.ESModule',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "ES Modules",
                id: -1
//                root: true
            },
            
            listeners:{
                load: 'onESModulesStoreLoad',
                scope: 'controller'
            }
        },
        parameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.ESModuleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    id: -1
    //                root: true
                },
            
                listeners: {
                    load: "onEsmodparamsLoad" 
                }
            
            }
    }

});
