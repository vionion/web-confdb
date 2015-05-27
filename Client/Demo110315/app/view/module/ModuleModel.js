Ext.define('Demo110315.view.module.ModuleModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.module-module',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true
    },
    
    requires:['Demo110315.model.Module',
             'Demo110315.model.Moduleitem'],
    
    stores:
    {        
        modules:{
            
            model:'Demo110315.model.Module',
            autoLoad: false,
            listeners:{
//                beforeload: function(){
//                    console.log("loading modules from model");
//                },
                load: 'onModulesStoreLoad',
                scope: 'controller'
            }
        },
        modparams:{ 
            
                type:'tree',
                model:'Demo110315.model.Moduleitem',
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
