Ext.define('Demo110315.view.edsource.EDSourceController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.edsource-edsource',
    
    onLoadEDSource: function(){
//        var tree = this.lookupReference('pathtab');
//        this.getViewModel().getStore('pathitems').load()
        
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        
//        cid, vid
        
        console.log("MOD ID CONF");
        console.log(idc);
        
        console.log("MOD ID VER");
        console.log(idv);
        
        if(cid !=-1){
            console.log("loading ed source cnf");
            this.getViewModel().getStore('edsource').load({params: {cnf: idc}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else if (vid !=-1){
            console.log("loading ed source ver");
            this.getViewModel().getStore('edsource').load({params: {ver: idv}});
//            this.lookupReference('modulesGrid').mask("Loading Modules"); 
        }
        else {
            console.log("ID CONF VER ERRORRRR");
        }
//        this.getViewModel().getStore('pathitems').getRoot().expand()
        
        
    },
    onEDSourceStoreLoad: function(store, records, successful, operation, node, eOpts){
        
        if(this.lookupReference('edSourceGrid').isMasked()){
            this.lookupReference('edSourceGrid').unmask();
        }
        
        store.getRoot().expand();
    }
    ,onGridEDSourceParamsForward: function(mid){
        
        //Ext.Msg.alert('onForward');
        console.log('in parent, got event');
        var grid = this.lookupReference('edSourceParamsTree');
        
        //var cid = this.getViewModel().get('currentModule').id;
        var vid = this.getViewModel().get("idVer");
        console.log('VID: ');
        console.log(vid);
        this.getViewModel().getStore('edsourceparams').load({params: {mid: mid}});

    }
    
    ,onEDSourceGridRender: function( view, eOpts ){
//        this.lookupReference('modulesGrid').mask("Loading Modules");
        view.mask("Loading ED Source");
    }
    
});
