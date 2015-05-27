Ext.define('Demo110315.view.esmodule.ESModuleController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.esmodule-esmodule',
    
    onLoadESModules: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load() cid, vid
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
        console.log("MOD ID CONF");
        console.log(idc);
        
        console.log("MOD ID VER");
        console.log(idv);
        
        if(idc !=-1){
            console.log("loading es modules cnf");
            this.getViewModel().getStore('esmodules').load({params: {cnf: idc}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else if (idv !=-1){
            console.log("loading es modules ver");
            this.getViewModel().getStore('esmodules').load({params: {ver: idv}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    onESModulesStoreLoad: function(store, records, successful, operation, node, eOpts){
        
        if(this.lookupReference('esModulesGrid').isMasked()){
            this.lookupReference('esModulesGrid').unmask();
        }
        
        store.getRoot().expand();
    }
    ,onGridESModParamsForward: function(mid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('esModParamsTree');
        
        //var cid = this.getViewModel().get('currentModule').id;
        var vid = this.getViewModel().get("idVer");
        console.log('VID: ');
        console.log(vid);
        this.getViewModel().getStore('esmodparams').load({params: {mid: mid}});
        
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
    
    ,onESModuleGridRender: function( view, eOpts ){
//        this.lookupReference('modulesGrid').mask("Loading Modules");
        view.mask("Loading ES Modules");
    }
});
