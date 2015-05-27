/**
 * This class is the main view for the application. It is specified in app.js as the
 * "autoCreateViewport" property. That setting automatically applies the "viewport"
 * plugin to promote that instance of this class to the body element.
 *
 * TODO - Replace this content of this view to suite the needs of your application.
 */
Ext.define('Demo110315.view.main.MainController', {
    extend: 'Ext.app.ViewController',

    requires: [
        'Ext.window.MessageBox'
    ],

    alias: 'controller.main',

    onClickButton: function () {
        Ext.Msg.confirm('Confirm', 'Are you sure?', 'onConfirm', this);
    },

    onConfirm: function (choice) {
        if (choice === 'yes') {
            //
        }
    },
    
    onExploreDatabaseForward: function(){
        
        var view = this.getView();
        console.log("In Main controller");
        
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
        
        view.insert(0,dbe);
        console.log(view.items);
        
        console.log("Removing");
        //Remove home
        var home = this.lookupReference('home');
        
        var foldersGrid = this.lookupReference('dbexplorer').lookupReference('foldersTree');
        foldersGrid.mask("Loading Folders");
        
        view.remove(home,true);
        console.log(view.items);
        
    },
    
    onCustFwdOpenLastVers: function(cid){
        
        var view = this.getView();
        console.log("In Main controller");
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
            }
         });
        
        dbe.getViewModel().set( "idCnf", cid );
        dbe.getViewModel().set( "idVer", -1 );
//        var pat = this.lookupReference('pathtab');
//        pat.getViewModel().set( "idVer", cid )
        console.log("DBE");
        console.log(dbe);
        view.insert(0,dbe);
        console.log(view.items);
        
        console.log("Removing Explorer");
        //Remove home
        var home = this.lookupReference('dbexplorer');
        view.remove(home,true);
        console.log(view.items);
    },
    
    onCustFwdOpenVer: function(vid){
        
        var view = this.getView();
        console.log("In Main controller");
        
        //Add Explorer
        var dbe =  Ext.create({
            xtype: 'confeditor',
            listeners:{
                backHome: 'onBackHome',
                exploreDatabase: 'onExploreDatabaseForward'
            }
         });
        
        dbe.getViewModel().set( "idVer", vid );
        dbe.getViewModel().set( "idCnf", -1 );
//        var pat = this.lookupReference('pathtab');
//        pat.getViewModel().set( "idVer", cid )
        
        view.insert(0,dbe);
        console.log(view.items);
        
        console.log("Removing Explorer");
        //Remove home
        var home = this.lookupReference('dbexplorer');
        view.remove(home,true);
        console.log(view.items);

    },
    
    onBackHome: function(){
        var view = this.getView();
        console.log("In Main controller");
        
        //Add Explorer
        var home =  Ext.create({
            xtype: 'home',
            listeners:{
                exploreDatabase: 'onExploreDatabaseForward'
            }
         });
        
        view.insert(0,home);
        console.log(view.items);
        
        console.log("Removing Editor");
        //Remove Editor
        var ceditor = this.lookupReference('confeditor');
        view.remove(ceditor,true);
        console.log(view.items);
        
    }
    
});
