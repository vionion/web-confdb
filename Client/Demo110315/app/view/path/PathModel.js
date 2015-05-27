Ext.define('Demo110315.view.path.PathModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.path-path',
    
    requires:['Demo110315.model.Pathitem',
             'Demo110315.model.Moduleitem',
             'Demo110315.model.Moduledetails',
             'Demo110315.model.Pathdetails'],
    
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true
    },
    
    stores:
    {        
        pathitems:{
            
            type:'tree',
            model:'Demo110315.model.Pathitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Paths",
                gid: -1
//                root: true
            },
            
            listeners: {

                load: 'onPathitemsLoad', 
                scope: 'controller',

//                load: function(store, records, successful, operation, node, eOpts){
////                    this.getViewModel().getStore('pathitems').getRoot().expand();
//                    
//                    var root_vid  =  this.getRoot().get('vid');
//                    console.log("ROOT_VID: ");
//                    console.log(root_vid);
//                    
//                    //Check if Version id in Root is still default: set Version id in Root
//                    if(root_vid == -1){
//                        //Check if The path list is empty
//                        if(records.length > 0){
//                            
//                                console.log(records[0].get('vid'));
//                                var verId = records[0].get('vid');
//                                this.getRoot().set('vid',verId);
//                                console.log("NEW ROOT_VID: ");
//                                console.log(root_vid);
//                            }
//                    }
//                    
////                    store.fireEvent('custSetVerId', verId);
////                    this.getRoot().expand();
//                },
                
                beforeload: 'onPathitemsBeforeLoad'
//                function(store, operation, eOpts) {
//
//                    var pi_type = operation.config.node.get('pit');
//                    
//                    operation.getProxy().setExtraParam('itype',pi_type);
//                    console.log(store.getRoot().get('vid'));
//                    operation.getProxy().setExtraParam('ver',store.getRoot().get('vid')); //operation.config.node.get('pit')
//                }
            }
        },
        parameters:{
            
                type:'tree',
                model:'Demo110315.model.Moduleitem',
                autoLoad:false,
            
                root: {
                    expanded: false,
                    text: "Params",
                    gid: -1
    //                root: true
                },
            
                listeners: {
                    
//                    beforeload: function(store, operation, eOpts) {
//                        var myRoot = store.getRoot()
//                        myRoot.removeAll(true)
//                    },
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
