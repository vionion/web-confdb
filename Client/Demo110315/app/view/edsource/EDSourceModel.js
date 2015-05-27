Ext.define('Demo110315.view.edsource.EDSourceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.edsource-edsource',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1
    },
    
    requires:['Demo110315.model.EDSource',
             'Demo110315.model.EDSourceitem'],
    
    stores:
    {        
        edsource:{
            
            type:'tree',
            model:'Demo110315.model.EDSource',
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
                model:'Demo110315.model.EDSourceitem',
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
