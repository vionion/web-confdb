Ext.define('CmsConfigExplorer.view.streamdataset.StreamDatasetController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-streamdataset',
    
    
    onStreamitemClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var sdView = this.getView();
        var central = this.lookupReference('streamCentralPanel');
        var centralLayout = central.getLayout(); 
        var item_type = record.get("s_type");
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
//        
//        var params = this.lookupReference('datasetPathsTree');
//        var pathDet = this.lookupReference('pathDetailsPanel');
        
        if(item_type == "dat"){
            
            
            centralLayout.setActiveItem(0);
            Ext.resumeLayouts(true);
            var dstid = record.get("gid");
            var name = record.get("name");
            
            this.getViewModel().set("current_dat",name);
//
//            console.log('in child, fwd event');
//            console.log(strid);
//            central.lookupReference('datasetpathsPanel')
//            console.log('sdView.getReferences()');
//            console.log(sdView.getReferences());
            
//            pathtreepanel = sdView.lookupReference('datasetpathsPanel');
            
            pathtreepanel = sdView.lookupReference('datasetPathsTree');
//            
//            console.log('pathtreepanel.getReferences()');
//            console.log(pathtreepanel.getReferences());
//            
//            console.log('pathtreepanel');
//            console.log(pathtreepanel);
            
            pathtree = pathtreepanel //.lookupReference('datasetPathsTree');
            
            pathtree.setLoading( "Loading Paths" );
            store = this.getViewModel().getStore('datasetpaths');
            if (store.isLoaded()){
                root = store.getRoot();
                root.removeAll();
            }
            store.getProxy().startParam = 0;
//            this.getViewModel().getStore('datasetpaths').
            store.load({params: {dstid: dstid, cnf: idc, ver: idv, online:online}});
            
//            console.log(store);

        }
        else if(item_type == "evc"){

            var strid = record.get("gid");
            var name = record.get("name");
            
            this.getViewModel().set("current_evc",name);

//            console.log("cusPatDetLoaded FIRED");
            centralLayout.setActiveItem(1);
            
//            this.getViewModel().getStore('ecstats').load({params: {strid: strid, cnf: idc, ver: idv}});
            
            this.getViewModel().getStore('ecstats').load({params: {strid: strid, online:online, verid: idv}});
        }
        
    },
    
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
            this.getViewModel().getStore('streamitems').load({params: {cnf: idc, online:online}});
        }
        else if (idv !=-1){
            this.getViewModel().getStore('streamitems').load({params: {ver: idv, online:online}});
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    
    
    onDatasetpathsLoad: function(store, records, successful, operation, node, eOpts) {
//                            var id = operation.config.node.get('gid')
//                            if (id == -1){
//                               operation.config.node.expand() 
        var sdView = this.getView();                     
//        pathtreepanel = sdView.lookupReference('datasetpathsPanel');
        pathtreepanel = sdView.lookupReference('datasetPathsTree');
        pathtree = pathtreepanel //.lookupReference('datasetPathsTree');   
        
        if(pathtree.isMasked()){
            pathtree.setLoading( false );
//            this.lookupReference('pathTree').unmask();
        }    
        store.getRoot().expand();
    }
    
    ,onStreamitemsBeforeLoad: function(store, operation, eOpts) {
        
        this.lookupReference('streamTree').setLoading("Loading Streams & Datasets");
    }
    
    ,onStreamitemsLoad: function(store, records, successful, operation, node, eOpts){
        
        if(this.lookupReference('streamTree').isMasked()){
            this.lookupReference('streamTree').setLoading(false);
        }
        
        store.getRoot().expand();
        
    }
    
});
