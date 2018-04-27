Ext.define('CmsConfigExplorer.view.globalpset.GlobalPsetController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.globalpset-globalpset',
    
//    onGridSrvParamsForward: function(sid){
//        
//        //Ext.Msg.alert('onForward');
//        console.log('in parent, got event');
//        var grid = this.lookupReference('srvParamsTree');
//        
//        this.getViewModel().getStore('srvparams').load({params: {sid: sid}});
//        
//    },
    
    onRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        //console.log("ID CONF");
        //console.log(idc);
        
        //console.log("ID VER");
        //console.log(idv);
        
        if(idc !=-1 && idc !=-2){
            this.getViewModel().getStore('gpsets').load({params: {cnf: idc, online:online}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('gpsets').load({params: {ver: idv, online:online}});
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    onGpsetClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sid = record.get("internal_id");
        var online = this.getViewModel().get("online");
        var idv = this.getViewModel().get("idVer");
//        var name = record.get("name");
        
        //console.log('in child, fwd event');
        //console.log(sid);
        
//        var serviceGrid = this.lookupReference('gpsettree');
//        serviceGrid.fireEvent('custSrvParams',sid);
        this.getViewModel().getStore('parameters').load({params: {set_id: sid, online:online, verid:idv}});
        
        var cp = this.lookupReference("centralGpsetPanel");
        
//        this.lookupReference("gpsetParamsTree").expand();
        
        var grid = this.lookupReference("paramGrid");
        grid.fireEvent( "cusTooltipActivate", grid );
        
        grid.setLoading("Loading Gpset Modules parameters");
    },
    
    onSortAlphaPaths: function(){
        
        var store = this.getViewModel().getStore('gpsets');      
        
        var sorter = Ext.create('Ext.util.Sorter',{
            sorterFn: function(record1, record2) {
            var pit1 = record1.data.pit;
            var pit2 = record2.data.pit;

            if (pit1 == 'pat' && pit2 == 'pat') {

                var name1 = record1.data.Name;
                var name2 = record2.data.Name;

                return name1 > name2 ? 1 : (name1 === name2) ? 0 : -1;
            }
            else {
                var ord1 = record1.data.order;
                var ord2 = record2.data.order;

                return ord1 > ord2 ? 1 : -1;
                }
            },
            direction: 'ASC'
        });

        var sorters = [];
        sorters.push(sorter);
        
        store.setSorters(sorters);
        store.sort('sorterFn');
        
        var pathTree = this.lookupReference('gpsettree');
        var tool = pathTree.lookupReference('gpsetHeaderTooolBar');

        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.disable();
        origButton.enable();
        
    },
    
    onSortOriginalPaths: function(){
        
        var store = this.getViewModel().getStore('gpsets');        
        
        //Sort By order

        var sorter = Ext.create('Ext.util.Sorter',{
            sorterFn: function(record1, record2) {
                var ord1 = record1.data.order;
                var ord2 = record2.data.order;

                return ord1 > ord2 ? 1 : -1;
            },
//                    property: 'order',
            direction: 'ASC'
        });

        var sorters = [];
        sorters.push(sorter);

        store.setSorters(sorters);
        store.sort('sorterFn');
        
        var pathTree = this.lookupReference('gpsettree');
        var tool = pathTree.lookupReference('gpsetHeaderTooolBar');
        
        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.enable();
        origButton.disable();
    }
    
    ,onGpsetsLoad: function(store, records, successful, operation, node, eOpts){
//                    this.getViewModel().getStore('pathitems').getRoot().expand();
        
        if(this.lookupReference('gpsetTree').isMasked()){
            this.lookupReference('gpsetTree').setLoading(false);
//            this.lookupReference('pathTree').unmask();
        }
        
        var root_vid  =  store.getRoot().get('vid');
        //console.log("ROOT_VID: ");
        //console.log(root_vid);

        //Check if Version id in Root is still default: set Version id in Root
        if(root_vid == -1){
            //Check if The path list is empty
            if(records.length > 0){

                    //console.log(records[0].get('vid'));
                    var verId = records[0].get('vid');
                    store.getRoot().set('vid',verId);
                    //console.log("NEW ROOT_VID: ");
                    //console.log(root_vid);
                }
        }

        store.getRoot().expand();
    }

    ,onGpsetsBeforeLoad: function(store, operation, eOpts) {
        
        this.lookupReference('gpsetTree').setLoading( "Loading Global Psets" );
        
    }
    
    ,onGpsetparamsLoad: function(store, records, successful, operation, node, eOpts) {
        var id = operation.config.node.get('id')
        if (id == -1){
           operation.config.node.expand() 
        }
        
        if(this.lookupReference("paramGrid").isMasked()){
            this.lookupReference("paramGrid").setLoading(false);
        }

    }
    
});
