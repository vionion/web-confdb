/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('CmsConfigExplorer.view.main.MainController', {
    extend: 'Ext.app.ViewController',

    requires: [
        'Ext.window.MessageBox',
        'CmsConfigExplorer.view.details.*',
        'CmsConfigExplorer.view.editor.*',
        'CmsConfigExplorer.view.summary.*',
        'CmsConfigExplorer.view.importconf.*'
    ],

    alias: 'controller.main',
    
    routes : {
        
//        'home' : 'onHome',
        'menu/:id' : 'onMenu'
    },
    
    onMenu : function(id) {
        var view = this.getView();
//        console.log("In ROUTE HANDLER");
//        console.log(id);
//        console.log(window.location.hash);
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
                
            }
         });
        
        var routeParams = [];
        
        routeParams = id.split("_");
        
        var verId = routeParams[0];
        var online =  routeParams[1];
        var appv =  this.getViewModel().get("appversion");
        
        dbe.getViewModel().set( "idVer", verId );
        dbe.getViewModel().set( "online", online );
        dbe.getViewModel().set( "idCnf", -2 );
        dbe.getViewModel().set( "appversion", appv);
//        var pat = this.lookupReference('pathtab');
//        pat.getViewModel().set( "idVer", cid )
        
        var ceditor = this.lookupReference('confeditor');
        
        if(ceditor!=null){
            view.remove(ceditor,true);
        }
        
//        var ceditor2 = this.lookupReference('confeditor');
//        if(ceditor2!=null){
//            view.remove(ceditor,true);
//            
//        }else {
//            console.log("AGAIN");
//        }
        
        view.insert(0,dbe);
        view.lookupReference('confeditor').lookupReference('cardspanel').getLayout().setActiveItem(0);
        
        //console.log("Removing Explorer");
        //Remove home
        var home = this.lookupReference('dbexplorer');
        view.remove(home,true);
        
        var scrollV, scrollH, loc = window.location;
        if ("pushState" in history)
            history.pushState("", document.title, loc.pathname + loc.search);
        else {
            // Prevent scrolling by storing the page's current scroll offset
            scrollV = document.body.scrollTop;
            scrollH = document.body.scrollLeft;

            loc.hash = "";

            // Restore the scroll offset, should be flicker free
            document.body.scrollTop = scrollV;
            document.body.scrollLeft = scrollH;
        }
        
        
        //console.log(view.items);
    },

    onClickButton: function () {
        Ext.Msg.confirm('Confirm', 'Are you sure?', 'onConfirm', this);
    },

    onConfirm: function (choice) {
        if (choice === 'yes') {
            //
        }
    },
    
    onImportPythonForward: function(){
        
        var view = this.getView();
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confimport',
            listeners:{
                backHome: 'onBackHome',
                cusOpenImportedFile: 'onOpenImportedFile'
//                custFwdOpenLastVers: 'onCustFwdOpenLastVers',
//                custFwdOpenVer: 'onCustFwdOpenVer'
            }
         });
        
        view.insert(0,dbe);

        //Remove home
        var home = this.lookupReference('home');
        
        //Remove editor if any
        var editor = this.lookupReference('confeditor');
        
        view.remove(home,true);
        
        if(editor != null){
            
            var summary = editor.lookupReference('summaryview');
            var details = editor.lookupReference('detailsview');
            
            if(summary != null){
                
                var biggrid = summary.lookupReference('biggrid');
                
                 if(biggrid != null){
                     
                    var status = biggrid.lookupReference('status');
                     
                    if(status != null){
                        
                        biggrid.remove(status,true);
                    }
                         
                    summary.remove(biggrid,true);
                 }
                
                editor.remove(summary,true);
            }
            
            if(details != null){
                editor.remove(details,true);
            }
            
            view.remove(editor,true);
        }
        
    },
    
    onExploreDatabaseForward: function(){
        
        var view = this.getView();
        //console.log("In Main controller");
        
//        view.remove("home",true);
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'dbexplorer',
            listeners:{
                backHome: 'onBackHome',
                custFwdOpenLastVers: 'onCustFwdOpenLastVers',
                custFwdOpenVer: 'onCustFwdOpenVer'
            }
         });
        
        var appv =  this.getViewModel().get("appversion");
        dbe.getViewModel().set( "appversion", appv);
        
        view.insert(0,dbe);
        //console.log(view.items);
        
        //console.log("Removing");
        //Remove home
        var home = this.lookupReference('home');
        
        //Remove editor if any
        var editor = this.lookupReference('confeditor');

        var foldersGrid = this.lookupReference('dbexplorer').lookupReference('foldersTree');
        foldersGrid.mask("Loading Folders");
        
        view.remove(home,true);
        //console.log(view.items);
        
        if(editor != null){
            
            var summary = editor.lookupReference('summaryview');
            var details = editor.lookupReference('detailsview');
            
            if(summary != null){
                
                var biggrid = summary.lookupReference('biggrid');
                
                 if(biggrid != null){
                     
                    var status = biggrid.lookupReference('status');
                     
                    if(status != null){
                        
                        biggrid.remove(status,true);
                    }
                         
                    summary.remove(biggrid,true);
                 }
                
                editor.remove(summary,true);
            }
            
            if(details != null){
                editor.remove(details,true);
            }
            
            view.remove(editor,true);
        }
        
    },
    
    onCustFwdOpenLastVers: function(cid,online){
        
        var view = this.getView();
        //console.log("In Main controller");
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
            }
         });
        
        var appv =  this.getViewModel().get("appversion");
        
        dbe.getViewModel().set( "online", online );
        dbe.getViewModel().set( "idCnf", cid );
        dbe.getViewModel().set( "idVer", -1 );
        dbe.getViewModel().set( "appversion", appv);
        view.insert(0,dbe);
             view.lookupReference('confeditor').lookupReference('cardspanel').getLayout().setActiveItem(0);

        //Remove home
        var home = this.lookupReference('dbexplorer');
        view.remove(home,true);
        //console.log(view.items);
    },
    
    onCustFwdOpenVer: function(vid,online){
        
        var view = this.getView();
        //console.log("In Main controller");
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
                
            }
         });
        
        var appv =  this.getViewModel().get("appversion");
        
        dbe.getViewModel().set( "idVer", vid );
        dbe.getViewModel().set( "online", online );
        dbe.getViewModel().set( "idCnf", -1 );
        dbe.getViewModel().set( "appversion", appv);
//        var pat = this.lookupReference('pathtab');
//        pat.getViewModel().set( "idVer", cid )
        
        view.insert(0,dbe);
        view.lookupReference('confeditor').lookupReference('cardspanel').getLayout().setActiveItem(0);
        
        //console.log("Removing Explorer");
        //Remove home
        var home = this.lookupReference('dbexplorer');
        view.remove(home,true);
        //console.log(view.items);

    },
    
    onOpenImportedFile: function(vid){
        
        var view = this.getView();
        //console.log("In Main controller");
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
                
            }
         });
        
        var appv =  this.getViewModel().get("appversion");
        
        dbe.getViewModel().set( "idVer", vid );
        dbe.getViewModel().set( "online", "file" );
        dbe.getViewModel().set( "idCnf", -1 );
        dbe.getViewModel().set( "appversion", appv);
//        var pat = this.lookupReference('pathtab');
//        pat.getViewModel().set( "idVer", cid )
        
        view.insert(0,dbe);
        view.lookupReference('confeditor').lookupReference('cardspanel').getLayout().setActiveItem(0);
        
        //console.log("Removing Explorer");
        //Remove home
        var home = this.lookupReference('confimport');
        view.remove(home,true);
        //console.log(view.items);

    },
    
    
    onBackHome: function(){
        var view = this.getView();
        //console.log("In Main controller");
        
        //Add Explorer
        var home =  Ext.create({
            xtype: 'home',
            listeners:{
                exploreDatabase: 'onExploreDatabaseForward',
                importPython: 'onImportPythonForward'
            }
         });
        var appv =  this.getViewModel().get("appversion");
        home.getViewModel().set( "appversion", appv);
        view.insert(0,home);
        //console.log(view.items);
        
        //console.log("Removing Editor");
        //Remove Editor
        var ceditor = this.lookupReference('confeditor');
        view.remove(ceditor,true);
        
        var cimport = this.lookupReference('confimport');
        view.remove(cimport,true);
        //console.log(view.items);
        
    }
    
    ,onBeforeHomeRender: function(view){
        var appv =  this.getViewModel().get("appversion");
        view.getViewModel().set( "appversion", appv);
    }
    
});
