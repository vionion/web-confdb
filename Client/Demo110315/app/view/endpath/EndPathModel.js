Ext.define('Demo110315.view.endpath.EndPathModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.endpath-endpath',
    
    requires:['Demo110315.model.Endpathitem'],
    
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true
    },
    
    stores:
    {        
        endpathitems:{
            
            type:'tree',
            model:'Demo110315.model.Endpathitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "End Paths",
                gid: -1
//                root: true
            },
            
            listeners: {

                load: 'onEndPathitemsLoad', 
                scope: 'controller',
                
                beforeload: 'onEndPathitemsBeforeLoad'

            }
        },
        endparameters:{
            
                type:'tree',
                model:'Demo110315.model.Moduleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Params",
                    gid: -1
                },
            
                listeners: {
                    
                    load: function(store, records, successful, operation, node, eOpts) {
                            var id = operation.config.node.get('gid');
                            if (id == -1){
                               operation.config.node.expand(); 
                            }
                    }
                }
            
            }
        
    }
});
