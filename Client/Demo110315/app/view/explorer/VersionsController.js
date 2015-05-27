Ext.define('Demo110315.view.explorer.VersionsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-versions',
    
    onVerDblClick: function(v, record, tr, rowIndex, e, eOpts){
        
//        if(record.get("fit") == "cnf"){
            var vid = record.get("gid");

            console.log('in fol cont, fwd event');
            console.log(vid);
            var view = this.getView();
            view.fireEvent('custOpenVer',vid);
//        }
    },
    
    onVerClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var textA = this.lookupReference('descTextArea');
        textA.setValue(record.get("description"));
    }
    
});
