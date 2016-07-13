Ext.define('CmsConfigExplorer.view.explorer.ExplorerController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-explorer',
    
//    onRender: function(p, eOpts){
//        console.log('LOADING FOLDERITEMS');
//        this.getViewModel().getStore('folderitems').load(); 
//        console.log('LOADED');
//    },
    
    onExplorerRender:function(p, eOpts){
        
        this.getViewModel().getStore('folderitems').load({params: {gid: -1}});
          
    },
    
    onHomeClick: function(){
            //console.log("In Explorer controller");
            var view = this.getView();
            view.fireEvent('backHome');
    },
    
    onForwaredOpenLastVers: function(cid,online){
        //console.log('in parent, got dblclick event');
        //console.log(cid);
        var view = this.getView();
        // var cid = (-1)*cid;
        view.fireEvent('custFwdOpenLastVers',cid,online);
    },
    
    onConfVersForward: function(cid, online){
        
        //console.log('in parent, got event');
//        var grid = this.lookupReference('versionsGrid');
        var textA = this.lookupReference('versionsPanel').lookupReference('descTextArea');
        textA.setValue("");
        this.getViewModel().getStore('versions').load({params: {cid: cid, online: online}});

    },
    
    onVerForward: function (vid,online){
        //console.log('in parent, got dblclick event');
        var view = this.getView();
        view.fireEvent('custFwdOpenVer',vid,online);
    }
    
//    ,onFolderItemsLoad: function( store, operation, eOpts ){
//        this.lookupReference('foldersTree').mask("Loading");
//    }
//    
    ,onFolderItemsLoad: function( store, records, successful, eOpts ){
        
        store.getRoot().expand();
        this.lookupReference('foldersTree').unmask();
    }
    
    ,onFoldertemsBeforeLoad: function(store, operation, eOpts) {
        
        var gid = operation.config.node.get('gid');
        
        var name = operation.config.node.get('name');
        var names = name.split("/");
        
        var online = 'False';
        var x;
        
        if (names[1] == 'cdaq' || names[1] == 'minidaq'){
            online = 'True';
        }
        
        
        operation.getProxy().setExtraParam('gid',gid);
        operation.getProxy().setExtraParam('online',online);
        
    }
    
    
});
