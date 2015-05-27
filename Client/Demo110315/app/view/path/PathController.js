Ext.define('Demo110315.view.path.PathController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-path',
    
    onRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        console.log("ID CONF");
        console.log(idc);
        
        console.log("ID VER");
        console.log(idv);
        
        if(idc !=-1){
            this.getViewModel().getStore('pathitems').load({params: {cnf: idc}});
            view = this.getView();
            
            view.fireEvent( "cusPathTabRender", idc, idv);
        }
        else if (idv !=-1){
            this.getViewModel().getStore('pathitems').load({params: {ver: idv}});
            view = this.getView();
            view.fireEvent( "cusPathTabRender", idc, idv);
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    onModParamsForward: function(mid,pid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('paramGrid');
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('parameters').load({params: {mid: mid, pid: pid}});
        
        var form = this.lookupReference('modDetails');
        form.fireEvent( "cusDetLoaded", mid, pid);
        
        console.log(form);
        
        
//        var form_vm = form.getViewModel();
//        
//        form_vm.getStore('moddetails').load({params: {mid: mid, pid: pid}});
        //var store = Ext.data.StoreManager.get("parameters"); 
        //console.log(store);
        //store.load({params:{id: cid}});
    },
    
    onPatDetForward: function(pid){
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        var form = this.lookupReference('pathDetailsPanel');
        form.fireEvent( "cusPatDetLoaded", pid,  idc, idv);
        console.log("cusPatDetLoaded FIRED");
        console.log(form);
    },
    
    onNodeClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var pathView = this.getView();
        var central = this.lookupReference('centralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("pit");
        
        var form = this.lookupReference('modDetails');
        var params = this.lookupReference('paramGrid');
        var pathDet = this.lookupReference('pathDetailsPanel');
        
        if(item_type == "mod"){
            
            centralLayout.setActiveItem(0);

            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            console.log('in child, fwd event');
            console.log(mid);
            var view = this.lookupReference('pathTree');
            view.fireEvent('custModParams',mid, pid);
        }
        else if(item_type == "pat"){
            
            var idc = this.getViewModel().get("idCnf");
            var idv = this.getViewModel().get("idVer");
            var pid = record.get("gid");

            pathDet.fireEvent( "cusPatDetLoaded", pid,  idc, idv);
            console.log("cusPatDetLoaded FIRED");
            
            centralLayout.setActiveItem(1);
        }
        
        
        
    }
    
    ,onPathitemsLoad: function( store, records, successful, eOpts ){
        
        if(this.lookupReference('pathTree').isMasked()){
            this.lookupReference('pathTree').setLoading( false );
//            this.lookupReference('pathTree').unmask();
        }
        
        var root_vid  =  store.getRoot().get('vid');
        console.log("ROOT_VID: ");
        console.log(root_vid);

        //Check if Version id in Root is still default: set Version id in Root
        if(root_vid == -1){
            //Check if The path list is empty
            if(records.length > 0){

                    console.log(records[0].get('vid'));
                    var verId = records[0].get('vid');
                    store.getRoot().set('vid',verId);
                    console.log("NEW ROOT_VID: ");
                    console.log(root_vid);
                }
        }

//                    store.fireEvent('custSetVerId', verId);
        store.getRoot().expand();
    },
    
    onPathitemsBeforeLoad: function(store, operation, eOpts) {

        var pi_type = operation.config.node.get('pit');
        
        operation.getProxy().setExtraParam('itype',pi_type);
        console.log(store.getRoot().get('vid'));
        operation.getProxy().setExtraParam('ver',store.getRoot().get('vid')); //operation.config.node.get('pit')
        
//        this.lookupReference('pathTree').mask();
        this.lookupReference('pathTree').setLoading( "Loading Paths" );
    }
    
//    ,onSetVerId: function(vId){
//        
////        var path = this.lookupReference('pathtab');
//        var idVer =  this.getViewModel().get('idVer')
//        if (idVer != -1){
//            this.getViewModel().set("idVer",vId);
//            this.getViewModel().getStore('pathitems').getRoot().set("vid",vId);
//        }
//    }
    
    
    
});
