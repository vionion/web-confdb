Ext.define('Demo110315.view.essource.ESSourceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.essource-essource',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1
    },
    
    requires:['Demo110315.model.ESSource',
             'Demo110315.model.ESSourceitem'],
    
    stores:
    {        
        essource:{
            
            type:'tree',
            model:'Demo110315.model.ESSource',
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
                model:'Demo110315.model.ESSourceitem',
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
