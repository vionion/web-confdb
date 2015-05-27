Ext.define('Demo110315.view.endpath.EndPathController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.endpath-endpath',
    
    onEndRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        console.log("ID CONF");
        console.log(idc);
        
        console.log("ID VER");
        console.log(idv);
        
        if(idc !=-1){
            this.getViewModel().getStore('endpathitems').load({params: {cnf: idc}});
            view = this.getView();
            
            view.fireEvent( "cusEndPathTabRender", idc, idv);
        }
        else if (idv !=-1){
            this.getViewModel().getStore('endpathitems').load({params: {ver: idv}});
            view = this.getView();
            view.fireEvent( "cusEndPathTabRender", idc, idv);
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    onEndModParamsForward: function(mid,pid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('endParamGrid');
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('endparameters').load({params: {mid: mid, pid: pid, epit: "mod"}});
        
        var form = this.lookupReference('endModDetails');
        form.fireEvent( "cusEndDetLoaded", mid, pid);
        
        console.log(form);
        
    },
    
    onEndOumModParamsForward: function(mid,pid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('endParamGrid');
        
        //var cid = this.getViewModel().get('currentModule').id;
        this.getViewModel().getStore('endparameters').load({params: {mid: mid, pid: pid, epit: "oum"}});
        
        var form = this.lookupReference('endModDetails');
        form.fireEvent( "cusEndOumDetLoaded", mid, pid);
        
        console.log(form);

    },
    
    onEndPatDetForward: function(pid){
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        var form = this.lookupReference('endPathDetailsPanel');
        form.fireEvent( "cusEndPatDetLoaded", pid,  idc, idv);
        console.log("cusEndPatDetLoaded FIRED");
        console.log(form);
    },
    
    onEndNodeClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var pathView = this.getView();
        var central = this.lookupReference('endCentralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("pit");
        
        var form = this.lookupReference('endModDetails');
        var params = this.lookupReference('endParamGrid');
        var pathDet = this.lookupReference('endPathDetailsPanel');
        
        if(item_type == "mod"){
            
            centralLayout.setActiveItem(0);

            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            console.log('in child, fwd event');
            console.log(mid);
            var view = this.lookupReference('endpathTree');
            view.fireEvent('cusEndModParams',mid, pid);
        }
        else if(item_type == "oum"){
            
            centralLayout.setActiveItem(0);

            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            console.log('in child, fwd event');
            console.log(mid);
            var view = this.lookupReference('endpathTree');
            view.fireEvent('cusEndOumModParams',mid, pid);
        }
        else if(item_type == "pat"){
            
            var idc = this.getViewModel().get("idCnf");
            var idv = this.getViewModel().get("idVer");
            var pid = record.get("gid");

            pathDet.fireEvent( "cusEndPatDetLoaded", pid,  idc, idv);
            console.log("cusEndPatDetLoaded FIRED");
            
            centralLayout.setActiveItem(1);
        }
        
    }
    
    ,onEndPathitemsLoad: function( store, records, successful, eOpts ){
        
        if(this.lookupReference('endpathTree').isMasked()){
            this.lookupReference('endpathTree').unmask();
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
    
    onEndPathitemsBeforeLoad: function(store, operation, eOpts) {

        var pi_type = operation.config.node.get('pit');
        
        operation.getProxy().setExtraParam('itype',pi_type);
        console.log(store.getRoot().get('vid'));
        operation.getProxy().setExtraParam('ver',store.getRoot().get('vid')); //operation.config.node.get('pit')
        
        this.lookupReference('endpathTree').mask();
    }
    
});
