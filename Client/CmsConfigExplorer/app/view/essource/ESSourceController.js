Ext.define('CmsConfigExplorer.view.essource.ESSourceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.essource-essource',
    
    onLoadESSource: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
//        cid, vid
        
        //console.log("MOD ID CONF");
        //console.log(idc);
        
        //console.log("MOD ID VER");
        //console.log(idv);
        
        if(cid !=-1 && cid !=-2){
            //console.log("loading es source cnf");
            this.getViewModel().getStore('essource').load({params: {cnf: idc, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else if (vid !=-1){
            //console.log("loading es source ver");
            this.getViewModel().getStore('essource').load({params: {ver: idv, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    onESSourceStoreLoad: function(store, records, successful, operation, node, eOpts){
        
//        if(this.lookupReference('esSourceGrid').isMasked()){
//            this.lookupReference('esSourceGrid').unmask();
//        }
        
        if(this.lookupReference('esSourceGrid').isMasked()){
            this.lookupReference('esSourceGrid').setLoading(false);
        }
        
        store.getRoot().expand();

    }
    ,onGridESSourceParamsForward: function(mid){
        
        //Ext.Msg.alert('onForward');
        //console.log('in parent, got event');
        var grid = this.lookupReference('paramGrid');
        var online = this.getViewModel().get("online");
        
        //var cid = this.getViewModel().get('currentModule').id;
        var vid = this.getViewModel().get("idVer");
        //console.log('VID: ');
        //console.log(vid);
        this.getViewModel().getStore('parameters').load({params: {mid: mid, online:online, verid:vid}});
        
        grid.fireEvent( "cusTooltipActivate", grid );
        
        grid.setLoading("Loading ES Source parameters");

    }
    
    ,onESSourceGridRender: function( view, eOpts ){
//        this.lookupReference('modulesGrid').mask("Loading Modules");
//        view.mask("Loading ES Source");
        this.lookupReference('esSourceGrid').setLoading( "Loading ES Source" );
    }
    
    ,onEssourceparamsLoad: function(store, records, successful, operation, node, eOpts) {
        var id = operation.config.node.get('gid')
        if (id == -1){
           operation.config.node.expand() 
        }
        
        if(this.lookupReference('paramGrid').isMasked()){
            this.lookupReference('paramGrid').setLoading(false);
        }
    }
                     
    
});
