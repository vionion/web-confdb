Ext.define('CmsConfigExplorer.view.service.ServiceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.service-service',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        first: true,
        prescaleLoaded: false,
        pathsloaded: false,
        online: "False",
        paths: []
    },
    
    requires:['CmsConfigExplorer.model.Service'
             ,'CmsConfigExplorer.model.Serviceitem'
             ],
    
    stores:
    {        

        services:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.Service',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "Services",
                gid: -1
//                root: true
            },
            
            listeners:{
                beforeload: function(){
                    //console.log("loading modules from model");
                },
                load: "onServicesLoad" 
            }
        },
        srvparams:{ 
            
                type:'tree',
                model:'CmsConfigExplorer.model.Serviceitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    gid: -1

    //                root: true
                },
            
                listeners: {
                    load: "onSrvparamsLoad"
                }
            
            }
    }
    
});
