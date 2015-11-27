Ext.define('CmsConfigExplorer.view.edsource.EDSourceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.edsource-edsource',
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        online: "False",
        idCnf: -1
    },
    
    requires:['CmsConfigExplorer.model.EDSource',
             'CmsConfigExplorer.model.EDSourceitem'],
    
    stores:
    {        
        edsource:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.EDSource',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "ED Source",
                gid: -1
//                root: true
            },
            
            listeners:{
                load: 'onEDSourceStoreLoad',
                scope: 'controller'
            }
        },
        edsourceparams:{ 
            
                type:'tree',
                model:'CmsConfigExplorer.model.EDSourceitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    gid: -1
    //                root: true
                },
            
                listeners: {
                    load: function(store, records, successful, operation, node, eOpts) {
                            var id = operation.config.node.get('gid')
                            if (id == -1){
                               operation.config.node.expand() 
                            }
                    }
                }
            
            }
    }


});
