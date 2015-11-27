Ext.define('CmsConfigExplorer.view.explorer.FoldersController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-folders',
    
    onConfClick: function( v, record, tr, rowIndex, e, eOpts) {
        
        if(record.get("fit") == "cnf"){
            var cid = record.get("gid");
            var name = record.get("name");
            
            var names = name.split("/");
        
            var online = 'False';
            var x;

            if (names[1] == 'cdaq' || names[1] == 'minidaq'){
                online = 'True';
            }

            //console.log('in child, fwd event');
            //console.log(cid);
            var view = this.getView();
            view.fireEvent('custConfVers',cid,online);
        }
        
    },
    
    onConfDblClick: function ( v, record, tr, rowIndex, e, eOpts ) {
        
        if(record.get("fit") == "cnf"){
            var cid = record.get("gid");
            
            var name = record.get("name");
            var names = name.split("/");
            var online = 'False';
            var x;

            if (names[1] == 'cdaq' || names[1] == 'minidaq'){
                online = 'True';
            }
            
            //console.log('in fol cont, fwd event');
            //console.log(cid);
            var view = this.getView();
            view.fireEvent('custOpenLastVers',cid,online);
        }
    }
    
});
