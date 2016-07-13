Ext.define('CmsConfigExplorer.view.module.ModuleController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.module-module',
    
    onLoadModules: function(){
//        var tree = this.lookupReference('pathtab'); cid, vid
//        this.getViewModel().getStore('pathitems').load()
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        if(cid !=-1 && cid !=-2){
            //console.log("loading modules cnf");
            this.getViewModel().getStore('modules').load({params: {cnf: idc, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
                        
        }
        else if (vid !=-1){
            //console.log("loading modules ver");
            this.getViewModel().getStore('modules').load({params: {ver: idv, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else {
            //console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    onModulesStoreLoad: function( store, records, successful, eOpts ){
        
//        var gm = this.getViewModel().get('gridMasked');
        
//        if(gm){
        
        var grid = this.lookupReference('modulesGrid');
        
//        console.log(grid.isMasked(true));
            
        if(grid.isMasked(true)){
//            this.lookupReference('modulesGrid').unmask();
            this.lookupReference('modulesGrid').setLoading( false ); 
        }
            
            var label = this.lookupReference('modulesGrid').lookupReference('modMatches');
            label.setValue(store.getCount());
            
//        }
        
    }
    ,onGridModParamsForward: function(mid){
        
        //Ext.Msg.alert('onForward');
        //console.log('in parent, got event');
        var grid = this.lookupReference('modParamsTree');
        
        //var cid = this.getViewModel().get('currentModule').id;
        var vid = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        //console.log('VID: ');
        //console.log(vid);
        this.getViewModel().getStore('modparams').load({params: {mid: mid, allmod:'true', online:online, verid: vid}});
        
        grid.setLoading("Loading Module parameters");
        
        grid.fireEvent( "cusTooltipActivate", grid );
        
//        var form = this.lookupReference('modDetails');
//        form.fireEvent( "cusDetLoaded", mid, pid);
//        
//        console.log(form);
        
        
//        var form_vm = form.getViewModel();
//        
//        form_vm.getStore('moddetails').load({params: {mid: mid, pid: pid}});
        //var store = Ext.data.StoreManager.get("parameters"); 
        //console.log(store);
        //store.load({params:{id: cid}});
    }
    
    ,onModuleGridRender: function( view, eOpts ){
        
        
        var grid = this.lookupReference('modulesGrid');
        var modStore = this.getViewModel().getStore('modules');
        
//        console.log(modStore.isLoaded());
            
        if(!modStore.isLoaded()){
//            this.lookupReference('modulesGrid').unmask();
//            this.lookupReference('modulesGrid').setLoading( false );
            this.lookupReference('modulesGrid').setLoading("Loading Modules");
        }
        
//        this.lookupReference('modulesGrid').setLoading("Loading Modules");
        
//        this.lookupReference('modulesGrid').mask("Loading Modules");
//        view.setConfig( {'loadingHeight': 100} );
//        view.mask("Loading Modules");
//        console.log(view.isVisible());
//        if (view.isVisible()){
//            view.setLoading( "Loading Modules" );
//            this.getViewModel().set('gridMasked',true);
//        }
    }
    
    ,onModparamsLoad: function(store, records, successful, operation, node, eOpts) {
        var id = operation.config.node.get('gid')
        if (id == -1){
           operation.config.node.expand() 
        }
        if(this.lookupReference('modParamsTree').isMasked()){
//            this.lookupReference('modulesGrid').unmask();
            this.lookupReference('modParamsTree').setLoading( false ); 
        }
    }
    
    ,onModulesStoreBeforeLoad: function(store, operation, eOpts ){
        
//        this.getView().setLoading("Loading Modules");
        
//        console.log(this.lookupReference('modulesGrid'));
//        var grid = this.lookupReference('modulesGrid');
//        grid.setLoading("Loading Modules");
//        this.lookupReference('modulesGrid').setLoading("Loading Modules");
        
//        
//        if (view.isVisible()){
//            view.setLoading( "Loading Modules" );
////            this.getViewModel().set('gridMasked',true);
//        }
    }
    
    
    
    
    
    
});
