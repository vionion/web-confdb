Ext.define('CmsConfigExplorer.view.essource.ESSourceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.essource-essource',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        online: "False",
        idCnf: -1
    },
    
    requires:['CmsConfigExplorer.model.ESSource',
             'CmsConfigExplorer.model.ESSourceitem'],
    
    stores:
    {        
        essource:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.ESSource',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "ES Source",
                id: -1
//                root: true
            },
            
            listeners:{
                load: 'onESSourceStoreLoad',
                scope: 'controller'
            }
        },
        parameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.ESSourceitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    id: -1
    //                root: true
                },
            
                listeners: {
                    load: "onEssourceparamsLoad" 
                }
            
            }
    }


});
