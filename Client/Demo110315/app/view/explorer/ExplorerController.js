Ext.define('Demo110315.view.explorer.ExplorerController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-explorer',
    
//    onRender: function(p, eOpts){
//        console.log('LOADING FOLDERITEMS');
//        this.getViewModel().getStore('folderitems').load(); 
//        console.log('LOADED');
//    },
    onHomeClick: function(){
            console.log("In Explorer controller");
            var view = this.getView();
            view.fireEvent('backHome');
    },
    
    onForwaredOpenLastVers: function(cid){
        console.log('in parent, got dblclick event');
        console.log(cid);
        var view = this.getView();
        view.fireEvent('custFwdOpenLastVers',cid);
    },
    
    onConfVersForward: function(cid){
        
        console.log('in parent, got event');
//        var grid = this.lookupReference('versionsGrid');
        var textA = this.lookupReference('versionsPanel').lookupReference('descTextArea');
        textA.setValue("");
        this.getViewModel().getStore('versions').load({params: {cid: cid}});

    },
    
    onVerForward: function (vid){
        console.log('in parent, got dblclick event');
        var view = this.getView();
        view.fireEvent('custFwdOpenVer',vid);
    }
    
//    ,onFolderItemsLoad: function( store, operation, eOpts ){
//        this.lookupReference('foldersTree').mask("Loading");
//    }
//    
    ,onFolderItemsLoad: function( store, records, successful, eOpts ){
        this.lookupReference('foldersTree').unmask();
    }
    
});
