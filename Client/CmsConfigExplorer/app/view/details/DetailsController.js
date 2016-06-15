Ext.define('CmsConfigExplorer.view.details.DetailsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.details-details',
    
    onBeforeRender: function(){
        
        cid = this.getViewModel().get("idCnf");
        
        var pat = this.lookupReference('pathtab');
        pat.getViewModel().set( "idCnf", cid );
        
        var vid = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");
        
        pat.getViewModel().set( "idVer", vid );
        pat.getViewModel().set( "online", online );
        
        var mod = this.lookupReference('moduleTab');
        mod.getViewModel().set( "idCnf", cid );
        mod.getViewModel().set( "idVer", vid );
        mod.getViewModel().set( "online", online );
//        
//        console.log("DETAILS!!!!");
//        console.log(vid);
  
    },
    
    onLoadPaths: function(store){
        
        var serviceTab = this.lookupReference('servicetab');
        var serviceVm = serviceTab.getViewModel();
        
        if(!serviceVm.get('pathsloaded')){
            
            var paths = []
            store.getRoot().cascadeBy( function(record) { 
                        if(record.get('pit') == 'pat'){
                            var p_obj = {}
                            p_obj.name = record.get('Name'); 
                            p_obj.order = record.get('order'); 
                            paths.push(p_obj); 
                        }
 
                    },this);
            
            serviceVm.set('paths',paths);
            serviceVm.set('pathsloaded',true);
            
        }
    },
    
    
    onPathTabRender: function(idc, idv, online){
        var sdTab = this.lookupReference('streamDatasetTab');
        var vm = sdTab.getViewModel();
        //console.log("Loading streams");
        vm.getStore('streamitems').load({params: {cnf: idc, ver: idv, online:online}});
        vm.set( "idCnf", cid );
        vm.set( "idVer", vid );
        vm.set( "online", online );

    },
    
    onBeforeTabChange: function(tabPanel, newCard, oldCard, eOpts){

        if(newCard.getConfig("title") == 'MODULES'){ 
            
            var cid = this.getViewModel().get("idCnf");
            var online = this.getViewModel().get("online");
        
            var pat = this.lookupReference('moduleTab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
//            console.log("DETAILS!!!!");
//            console.log(vid);
            
            pat.getViewModel().set( "online", online );

            }
        
        else if (newCard.getConfig("title") == 'PATHS') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('pathtab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
            
        }
        
        else if (newCard.getConfig("title") == 'END PATHS') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('endpathtab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'SERVICES') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('servicetab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'STREAMS & DATASETS') {

            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('streamDatasetTab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'ES MODULES') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('esModuleTab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'ED SOURCE') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('edSourceTab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'ES SOURCES') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('esSourceTab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
        
        else if (newCard.getConfig("title") == 'SEQUENCES') {
            
            var cid = this.getViewModel().get("idCnf");
            var vid = this.getViewModel().get("idVer");
            var online = this.getViewModel().get("online");
            
            var seqTab = this.lookupReference('sequenceTab');
            
            seqTab.getViewModel().set( "idCnf", cid );
            seqTab.getViewModel().set( "idVer", vid );
            seqTab.getViewModel().set( "online", online );
            
        }
        
        else if (newCard.getConfig("title") == 'GLOBAL PSET') {
            
            var cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('globalpsettab');
            pat.getViewModel().set( "idCnf", cid );

            var vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            
            var online = this.getViewModel().get("online");
            pat.getViewModel().set( "online", online );
        }
    }
    
});
