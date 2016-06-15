Ext.define('CmsConfigExplorer.view.globalpset.GlobalPsetModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.globalpset-globalpset',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        online: "False"
    },
    
    requires:['CmsConfigExplorer.model.GlobalPset',
             'CmsConfigExplorer.model.GlobalPsetItem'],
    
    stores:
    {        
        gpsets:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.GlobalPset',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "Global Pset",
                gid: -1
//                root: true
            },
            
            listeners:{
                beforeload: 'onGpsetsBeforeLoad', 
                load: 'onGpsetsLoad',
                scope: 'controller'
            }
        },
        gpsetparams:{ 
            
                type:'tree',
                model:'CmsConfigExplorer.model.GlobalPsetItem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    gid: -1

    //                root: true
                },
            
                listeners: {
                    load: 'onGpsetparamsLoad'
                }
            
            }
    }
    

});
