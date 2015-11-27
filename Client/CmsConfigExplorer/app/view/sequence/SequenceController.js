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
    },
    
    onSequenceRender: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
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
        
    }
    
    
});
