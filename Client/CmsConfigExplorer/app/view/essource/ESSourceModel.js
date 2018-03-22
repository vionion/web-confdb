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
                gid: -1
//                root: true
            },
            
            listeners:{
                load: 'onESSourceStoreLoad',
                scope: 'controller'
            }
        },
        essourceparams:{ 
            
                type:'tree',
                model:'CmsConfigExplorer.model.ESSourceitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    gid: -1
    //                root: true
                },
            
                listeners: {
                    load: "onEssourceparamsLoad" 
                }
            
            }
    }


});
