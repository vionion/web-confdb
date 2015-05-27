Ext.define('Demo110315.view.editor.EditorController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.editor-editor',
    
    onBeforeRender: function(){
        
        cid = this.getViewModel().get("idCnf");
        
        var pat = this.lookupReference('pathtab');
        pat.getViewModel().set( "idCnf", cid );
        
        vid = this.getViewModel().get("idVer");
        pat.getViewModel().set( "idVer", vid );
        
        this.getViewModel().getStore('cnfdetails').load({params: {cnf: cid, ver: vid}});
    },
    
    onHomeClick: function(){
            console.log("In Editor controller");
            var view = this.getView();
            view.fireEvent('backHome');
    },
    
    onExploreClick: function(){
            console.log("In Editor controller");
            var view = this.getView();
            view.fireEvent('exploreDatabase');
    },
    
    onPathTabRender: function(idc, idv){
        var sdTab = this.lookupReference('streamDatasetTab');
        var vm = sdTab.getViewModel();
        console.log("Loading streams");
        vm.getStore('streamitems').load({params: {cnf: idc, ver: idv}});
        vm.set( "idCnf", cid );
        vm.set( "idVer", vid );

    },
    
    onBeforeTabChange: function(tabPanel, newCard, oldCard, eOpts){
        
        console.log("In Editor controller OUT MODTAB");
        console.log(newCard.getConfig("title"));
        
        if(newCard.getConfig("title") == 'MODULES'){ 
        
                console.log("In Editor controller MODTAB");
//                cid = this.getViewModel().get("idCnf");
//
//                var mod = this.lookupReference('moduleTab');
////                mod.getViewModel().set( "idCnf", cid );
//
//                vid = this.getViewModel().get("idVer");
//
//                
//                newCard.fireEvent('loadModules',cid, vid);
//
//                mod.getViewModel().getStore('modules').load({params: {cnf: cid, ver: vid}});
//                mod.getViewModel().set( "idVer", vid );
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('moduleTab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );

            }
        
        else if (newCard.getConfig("title") == 'PATHS') {
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('pathtab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
        }
        
        else if (newCard.getConfig("title") == 'END PATHS') {
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('endpathtab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
        }
        
        else if (newCard.getConfig("title") == 'SERVICES') {
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('servicetab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
        }
        
        else if (newCard.getConfig("title") == 'STREAMS & DATASETS') {
            
//            cid = this.getViewModel().get("idCnf");
//            vid = this.getViewModel().get("idVer");
//            
//            var sdTab = this.lookupReference('streamDatasetTab');
//            var vm = sdTab.getViewModel();
//            console.log("Loading streams");
//            vm.getStore('streamitems').load({params: {cnf: cid, ver: vid}});
//            console.log("Loaded streams");
//            
////            sdTab.lookupReference('streamTree').getRootNode().expand();
//            vm.set( "idCnf", cid );
//            vm.set( "idVer", vid );
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('streamDatasetTab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            

        }
        
        else if (newCard.getConfig("title") == 'ES MODULES') {
            
//            cid = this.getViewModel().get("idCnf");
//            vid = this.getViewModel().get("idVer");
//            
//            var esmTab = this.lookupReference('esModuleTab');
//            var vm = esmTab.getViewModel();
//            console.log("Loading ESM Modules");
//            vm.getStore('esmodules').load({params: {cnf: cid, ver: vid}});
//            console.log("Loaded ESM Modules");
//            
//            vm.set( "idCnf", cid );
//            vm.set( "idVer", vid );
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('esModuleTab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            

        }
        
        else if (newCard.getConfig("title") == 'ED SOURCE') {
            
//            cid = this.getViewModel().get("idCnf");
//            vid = this.getViewModel().get("idVer");
//            
//            var esmTab = this.lookupReference('edSourceTab');
//            var vm = esmTab.getViewModel();
//            console.log("Loading ED Source");
//            vm.getStore('edsource').load({params: {cnf: cid, ver: vid}});
//            console.log("Loaded ED Source");
//            
//            vm.set( "idCnf", cid );
//            vm.set( "idVer", vid );
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('edSourceTab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            

        }
        
        else if (newCard.getConfig("title") == 'ES SOURCES') {
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('esSourceTab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
            

        }
        
        else if (newCard.getConfig("title") == 'SEQUENCES') {
            
//            cid = this.getViewModel().get("idCnf");
//            vid = this.getViewModel().get("idVer");
//            
//            var esmTab = this.lookupReference('sequenceTab');
//            var vm = esmTab.getViewModel();
//            console.log("Loading Sequences");
//            vm.getStore('seqitems').load({params: {cnf: cid, ver: vid}});
//            console.log("Loaded Sequences");
//            
//            vm.set( "idCnf", cid );
//            vm.set( "idVer", vid );

        }
        
        else if (newCard.getConfig("title") == 'GLOBAL PSET') {
            
            cid = this.getViewModel().get("idCnf");
        
            var pat = this.lookupReference('globalpsettab');
            pat.getViewModel().set( "idCnf", cid );

            vid = this.getViewModel().get("idVer");
            pat.getViewModel().set( "idVer", vid );
        }
    },
    
    onCnfDetailsLoad: function( store, records, successful, eOpts ){
        det = records[0];
        name = det.get("name");
        this.getViewModel().set( "cnfname", name );
    }
    
    
});
