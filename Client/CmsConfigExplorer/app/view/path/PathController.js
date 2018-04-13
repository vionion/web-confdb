Ext.define('CmsConfigExplorer.view.path.PathController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-path',
    
    onRender: function(){

        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        if(idc !=-1){
            this.getViewModel().getStore('pathitems').load({params: {cnf: idc, online:online}});
            view = this.getView();
            
            view.fireEvent( "cusPathTabRender", idc, idv, online);
        }
        else if (idv !=-1){
            this.getViewModel().getStore('pathitems').load({params: {ver: idv, online:online}});
            view = this.getView();
            view.fireEvent( "cusPathTabRender", idc, idv, online);
        }
        else {
        }
//        
    },
    
    onDetailsRender: function(){

        var pl = this.getViewModel().get("pathsLoaded");
        
        if (!pl){
            
            var idc = this.getViewModel().get("idCnf");
            var idv = this.getViewModel().get("idVer");
            var online = this.getViewModel().get("online");
            
//            console.log("DETAILS RENDER!!!! - IDV - IDC");
//            console.log(idv);
//            console.log(idc);
        
            if(idc !=-1 && idc !=-2){
                this.getViewModel().getStore('pathitems').load({params: {cnf: idc, online:online}});
                view = this.getView();

                view.fireEvent( "cusPathTabRender", idc, idv, online);
            }
            else if (idv !=-1){
                this.getViewModel().getStore('pathitems').load({params: {ver: idv, online:online}});
                view = this.getView();
                view.fireEvent( "cusPathTabRender", idc, idv, online);
            }
            else {
                //console.log("ID CONF VER ERRORRRR");
            }
            
            this.getViewModel().set("pathsLoaded",true);
        }
    },
    
    onSortAlphaPaths: function(){
        
        var store = this.getViewModel().getStore('pathitems');      
        
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
        
        var pathTree = this.lookupReference('pathTree');
        var tool = pathTree.lookupReference('pathHeaderTooolBar');

        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.disable();
        origButton.enable();
        
    },
    
    onSortOriginalPaths: function(){
        
        var store = this.getViewModel().getStore('pathitems');        
        
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
        
        var pathTree = this.lookupReference('pathTree');
        var tool = pathTree.lookupReference('pathHeaderTooolBar');
        
        var alphaButton = tool.items.getAt(2); 
        var origButton = tool.items.getAt(3);
        
        alphaButton.enable();
        origButton.disable();
    }

    ,onPathColumnNameHeaderClickForward: function( ct, column, e, t, eOpts ){
        
        var store = this.getViewModel().getStore('pathitems');        
        
        if (this.getViewModel().get('sortToogle')){
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
            
            this.getViewModel().set('sortToogle',false);
        }
        else{
            //Sort By Name
            
            var sorter = Ext.create('Ext.util.Sorter',{
                sorterFn: function(record1, record2) {
                var pit1 = record1.data.pit;
                var pit2 = record2.data.pit;

                if (pit1 == 'pat' && pit2 == 'pat') {

                    var name1 = record1.data.name;
                    var name2 = record2.data.name;

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
            
            this.getViewModel().set('sortToogle',true);
        }
            
        
    },
    
    onModParamsForward: function(mid,pid){

        var grid = this.lookupReference('paramGrid');
        var online = this.getViewModel().get("online");
        var idv = this.getViewModel().get("idVer");
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('parameters').load({params: {mid: mid, pid: pid, online:online, verid:idv}});
        this.lookupReference('paramGrid').setLoading("Loading Module Parameters");
        
        var form = this.lookupReference('modDetails');
        form.fireEvent( "cusDetLoaded", mid, pid, online,idv);
        
        //console.log(form);
        
        grid.fireEvent( "cusTooltipActivate", grid );
        
    },
    
    onPatDetForward: function(pid){
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        var form = this.lookupReference('pathDetailsPanel');
        form.fireEvent( "cusPatDetLoaded", pid,  idc, idv, online);
        //console.log("cusPatDetLoaded FIRED");
        //console.log(form);
    },
    
    onNodeClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var pathView = this.getView();
        var online = this.getViewModel().get("online");
        var central = this.lookupReference('centralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("pit");

        var pathDet = this.lookupReference('pathDetailsPanel');
        
        if(item_type == "mod"){
            
            centralLayout.setActiveItem(0);

            var mid = record.get("internal_id");
            var pid = record.get("id_pathid");

            //console.log('in child, fwd event');
            //console.log(mid);
            var view = this.lookupReference('pathTree');
            view.fireEvent('custModParams',mid, pid, online);
        }
        else if(item_type == "pat"){
            
            var idc = this.getViewModel().get("idCnf");
            var idv = this.getViewModel().get("idVer");
            var pid = record.get("internal_id");

            pathDet.fireEvent( "cusPatDetLoaded", pid,  idc, idv, online);
            //console.log("cusPatDetLoaded FIRED");
            
            centralLayout.setActiveItem(1);
        }
        
        
        
    }
    
    ,onPathitemsLoad: function( store, records, successful, eOpts ){
        
        if(this.lookupReference('pathTree').isMasked()){
            this.lookupReference('pathTree').setLoading( false );
//            this.lookupReference('pathTree').unmask();
        }
        
        this.getView().fireEvent('loadPaths',store);

        var root_vid = store.getRoot().get('vid');
        //Check if Version id in Root is still default: set Version id in Root
        if(root_vid == -1){
            //Check if The path list is empty
            if(records.length > 0){
                    var verId = records[0].get('vid');
                    store.getRoot().set('vid',verId);
                }
        }

//                    store.fireEvent('custSetVerId', verId);
        store.getRoot().expand();
    },

    onPathitemsBeforeLoad: function(store, operation, eOpts) {
        var pi_type = operation.config.node.get('pit');
        var online = this.getViewModel().get("online");
        operation.getProxy().setExtraParam('online',online);
        operation.getProxy().setExtraParam('itype',pi_type);
        operation.getProxy().setExtraParam('ver',store.getRoot().get('vid'));
        operation.getProxy().setExtraParam('node',operation.node.data.internal_id);
        this.lookupReference('pathTree').setLoading( "Loading Paths" );
    }
    
    ,onPathModuleParametersLoad: function(store, records, successful, operation, node, eOpts) {
            var id = operation.config.node.get('id')
            if (id == -1){
               operation.config.node.expand() 
            }
        
            if(this.lookupReference('paramGrid').isMasked()){
                this.lookupReference('paramGrid').setLoading(false);
            }
    }
    
});
