Ext.define('CmsConfigExplorer.view.sequence.SequenceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.sequence-sequence',
    
    onSeqitemsBeforeLoad: function(store, operation, eOpts) {
//
//        var pi_type = operation.config.node.get('pit');
//        
//        operation.getProxy().setExtraParam('itype',pi_type);
//        console.log(store.getRoot().get('vid'));
//        operation.getProxy().setExtraParam('ver',store.getRoot().get('vid')); //operation.config.node.get('pit')
//        
//        this.lookupReference('pathTree').mask();
    }
    
    ,onSeqitemsLoad: function( store, records, successful, eOpts ){
        
        store.getRoot().expand();
        if(this.lookupReference('seqTree').isMasked()){
            this.lookupReference('seqTree').setLoading(false);
        }
    },
    
    onSequenceRender: function(){
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        if(idc !=-1 && idc !=-2){
            this.getViewModel().getStore('seqitems').load({params: {cnf: idc, online:online}});
//            view = this.getView();
            
//            view.fireEvent( "cusEndPathTabRender", idc, idv, online);
        }
        else if (idv !=-1){
            this.getViewModel().getStore('seqitems').load({params: {ver: idv, online:online}});
//            view = this.getView();
//            view.fireEvent( "cusEndPathTabRender", idc, idv, online);
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
        
        this.lookupReference('seqTree').setLoading( "Loading Sequences" );
        
        //console.log("ID CONF");
        //console.log(idc);
        
        //console.log("ID VER");
        //console.log(idv);
        
//        if(idc !=-1){
//            this.getViewModel().getStore('seqitems').load({params: {cnf: idc}});
//            view = this.getView();
////            
////            view.fireEvent( "cusPathTabRender", idc, idv);
//        }
//        else if (idv !=-1){
//            this.getViewModel().getStore('seqitems').load({params: {ver: idv}});
////            view = this.getView();
////            view.fireEvent( "cusPathTabRender", idc, idv);
//        }
//        else {
//            console.log("ID CONF VER ERRORRRR");
//        }
////        this.getViewModel().getStore('pathitems').getRoot().expand()
//        
        
    }
    ,onSequenceNodeClick: function(v, record, tr, rowIndex, e, eOpts){
        
//        var pathView = this.getView();
//        var online = this.getViewModel().get("online");
//        var central = this.lookupReference('centralPanel');
//        var centralLayout = central.getLayout(); 
//        
//        
//        var form = this.lookupReference('modDetails');
//        var params = this.lookupReference('paramGrid');
//        var pathDet = this.lookupReference('pathDetailsPanel');
        
        
        var item_type = record.get("pit");
        
        if(item_type == "mod"){

            // var mid = record.get("orig_id");
            var mid = record.get("gid");
            var m_int = parseInt(mid);
            // m_int = (-1)*m_int;
            mid = m_int;
            
            var pid = record.get("id_pathid");
            var online = this.getViewModel().get("online");
            var idv = this.getViewModel().get("idVer");
            var idc = this.getViewModel().get("idCnf");

            //console.log('in child, fwd event');
            //console.log(mid);
            this.getViewModel().getStore('parameters').load({params: {mid: mid, pid: pid, online:online, verid:idv, cnf:idc}});
//            view.fireEvent('custModParams',mid, pid, online);
            
            this.lookupReference('paramGrid').setLoading("Loading Module Parameters");
            
            var form = this.lookupReference('seqModDetails');
            form.fireEvent( "cusSeqModDetLoad", mid, pid, online,idv, idc);
            
        }
  
        
//        //console.log(form);
//        
//        grid.fireEvent( "cusTooltipActivate", grid );
        
        
        
    }
    
    ,onSeqparametersLoad: function(store, records, successful, operation, node, eOpts) {
        var id = operation.config.node.get('gid')
        if (id == -1){
           operation.config.node.expand() 
        }
        
        if(this.lookupReference('paramGrid').isMasked()){
                this.lookupReference('paramGrid').setLoading( false );
        }
    }
});
