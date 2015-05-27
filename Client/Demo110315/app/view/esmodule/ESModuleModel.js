Ext.define('Demo110315.view.esmodule.ESModuleModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.esmodule-esmodule',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true
    },
    
    requires:['Demo110315.model.ESModule',
             'Demo110315.model.ESModuleitem'],
    
    stores:
    {        
        esmodules:{
            
            type:'tree',
            model:'Demo110315.model.ESModule',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "ES Modules",
                gid: -1
//                root: true
            },
            
            listeners:{
                load: 'onESModulesStoreLoad',
                scope: 'controller'
            }
        },
        esmodparams:{ 
            
                type:'tree',
                model:'Demo110315.model.ESModuleitem',
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
