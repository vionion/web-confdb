Ext.define('Demo110315.view.globalpset.GlobalPsetModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.globalpset-globalpset',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1
    },
    
    requires:['Demo110315.model.GlobalPset',
             'Demo110315.model.GlobalPsetItem'],
    
    stores:
    {        
        gpsets:{
            
            type:'tree',
            model:'Demo110315.model.GlobalPset',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "Global Pset",
                gid: -1
//                root: true
            },
            
            listeners:{
                beforeload: function(){
                    console.log("loading modules from model");
                },
                load: function(store, records, successful, operation, node, eOpts){
//                    this.getViewModel().getStore('pathitems').getRoot().expand();
                    
                    var root_vid  =  this.getRoot().get('vid');
                    console.log("ROOT_VID: ");
                    console.log(root_vid);
                    
                    //Check if Version id in Root is still default: set Version id in Root
                    if(root_vid == -1){
                        //Check if The path list is empty
                        if(records.length > 0){
                            
                                console.log(records[0].get('vid'));
                                var verId = records[0].get('vid');
                                this.getRoot().set('vid',verId);
                                console.log("NEW ROOT_VID: ");
                                console.log(root_vid);
                            }
                    }
                    
                    this.getRoot().expand();
                }
            }
        },
        gpsetparams:{ 
            
                type:'tree',
                model:'Demo110315.model.GlobalPsetItem',
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
