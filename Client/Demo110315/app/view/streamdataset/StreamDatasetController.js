Ext.define('Demo110315.view.streamdataset.StreamDatasetController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-streamdataset',
    
    
    onStreamitemClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sdView = this.getView();
        var central = this.lookupReference('streamCentralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("s_type");
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
//        
//        var params = this.lookupReference('datasetPathsTree');
//        var pathDet = this.lookupReference('pathDetailsPanel');
        
        if(item_type == "dat"){
            
            
            centralLayout.setActiveItem(0);
            Ext.resumeLayouts(true);
            var dstid = record.get("gid");
//
//            console.log('in child, fwd event');
//            console.log(strid);
//            central.lookupReference('datasetpathsPanel')
//            console.log('sdView.getReferences()');
//            console.log(sdView.getReferences());
            
            pathtreepanel = sdView.lookupReference('datasetpathsPanel');
//            
//            console.log('pathtreepanel.getReferences()');
//            console.log(pathtreepanel.getReferences());
//            
//            console.log('pathtreepanel');
//            console.log(pathtreepanel);
            
            pathtree = pathtreepanel.lookupReference('datasetPathsTree');
            
            pathtree.setLoading( "Loading Paths" );
            store = this.getViewModel().getStore('datasetpaths');
            if (store.isLoaded()){
                root = store.getRoot();
                root.removeAll();
            }
            store.getProxy().startParam = 0;
//            this.getViewModel().getStore('datasetpaths').
            store.load({params: {dstid: dstid, cnf: idc, ver: idv}});
            
            console.log(store);

        }
        else if(item_type == "evc"){

            var strid = record.get("gid");

//            console.log("cusPatDetLoaded FIRED");
            centralLayout.setActiveItem(1);
            
//            this.getViewModel().getStore('ecstats').load({params: {strid: strid, cnf: idc, ver: idv}});
            
            this.getViewModel().getStore('ecstats').load({params: {strid: strid}});
        }
        
    },
    
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
            this.getViewModel().getStore('streamitems').load({params: {cnf: idc}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('streamitems').load({params: {ver: idv}});
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    
    onDatasetpathsLoad: function(store, records, successful, operation, node, eOpts) {
//                            var id = operation.config.node.get('gid')
//                            if (id == -1){
//                               operation.config.node.expand() 
        var sdView = this.getView();                     
        pathtreepanel = sdView.lookupReference('datasetpathsPanel');
        pathtree = pathtreepanel.lookupReference('datasetPathsTree');   
        
        if(pathtree.isMasked()){
            pathtree.setLoading( false );
//            this.lookupReference('pathTree').unmask();
        }    
        store.getRoot().expand();
    }
    
    
    
    
});
