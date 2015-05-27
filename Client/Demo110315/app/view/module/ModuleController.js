Ext.define('Demo110315.view.module.ModuleController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.module-module',
    
    onLoadModules: function(){
//        var tree = this.lookupReference('pathtab'); cid, vid
//        this.getViewModel().getStore('pathitems').load()
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        console.log("MOD ID CONF");
        console.log(idc);
        
        console.log("MOD ID VER");
        console.log(idv);
        
        if(cid !=-1){
            console.log("loading modules cnf");
            this.getViewModel().getStore('modules').load({params: {cnf: idc}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else if (vid !=-1){
            console.log("loading modules ver");
            this.getViewModel().getStore('modules').load({params: {ver: idv}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    onModulesStoreLoad: function( store, records, successful, eOpts ){
        
        if(this.lookupReference('modulesGrid').isMasked()){
//            this.lookupReference('modulesGrid').unmask();
            this.lookupReference('modulesGrid').setLoading( false ); 
        }
    }
    ,onGridModParamsForward: function(mid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('modParamsTree');
        
        //var cid = this.getViewModel().get('currentModule').id;
        var vid = this.getViewModel().get("idVer");
        console.log('VID: ');
        console.log(vid);
        this.getViewModel().getStore('modparams').load({params: {mid: mid}});
        
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
//        this.lookupReference('modulesGrid').mask("Loading Modules");
//        view.setConfig( {'loadingHeight': 100} );
//        view.mask("Loading Modules");
        view.setLoading( "Loading Modules" );
    }
    
    
    
    
    
});
