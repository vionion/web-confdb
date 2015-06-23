Ext.define('Demo110315.view.service.ServiceModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.service-service',
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true,
        prescaleLoaded: false
    },
    
    requires:['Demo110315.model.Service'
             ,'Demo110315.model.Serviceitem'
             ],
    
    stores:
    {        
        services:{
            
            type:'tree',
            model:'Demo110315.model.Service',
            autoLoad: false,
            
            root: {
                expanded: false,
                text: "Services",
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
        srvparams:{ 
            
                type:'tree',
                model:'Demo110315.model.Serviceitem',
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
