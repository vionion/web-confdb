Ext.define('CmsConfigExplorer.view.module.ModuleModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.module-module',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        first: true,
        online: "False",
        gridMasked: false
    },
    
    requires:['CmsConfigExplorer.model.Module',
             'CmsConfigExplorer.model.Moduleitem'],
    
    stores:
    {        
        modules:{
            
            model:'CmsConfigExplorer.model.Module',
            autoLoad: false,
            listeners:{
                beforeload: 'onModulesStoreBeforeLoad',
                load: 'onModulesStoreLoad',
                scope: 'controller'
            }
        },
        // inputTags:{
        //     model:'CmsConfigExplorer.model.InputTag',
        //     autoLoad: false
        // },
        parameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.Moduleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    id: -1
    //                root: true
                },
            
                listeners: {
                    load: "onModparamsLoad" 
                }
            
            }
    }

});
