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
                id: -1
//                root: true
            },
            
            listeners:{
                load: 'onEDSourceStoreLoad',
                scope: 'controller'
            }
        },
        parameters:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.EDSourceitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Parameters",
                    id: -1
    //                root: true
                },
            
                listeners: {
                    load: function(store, records, successful, operation, node, eOpts) {
                            var id = operation.config.node.get('id')
                            if (id == -1){
                               operation.config.node.expand() 
                            }
                    }
                }
            
            }
    }


});
