Ext.define('Demo110315.view.explorer.FoldersController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-folders',
    
    onConfClick: function( v, record, tr, rowIndex, e, eOpts) {
        
        if(record.get("fit") == "cnf"){
            var cid = record.get("gid");

            console.log('in child, fwd event');
            console.log(cid);
            var view = this.getView();
            view.fireEvent('custConfVers',cid);
        }
        
    },
    
    onConfDblClick: function ( v, record, tr, rowIndex, e, eOpts ) {
        
        if(record.get("fit") == "cnf"){
            var cid = record.get("gid");

            console.log('in fol cont, fwd event');
            console.log(cid);
            var view = this.getView();
            view.fireEvent('custOpenLastVers',cid);
        }
    }
    
});
