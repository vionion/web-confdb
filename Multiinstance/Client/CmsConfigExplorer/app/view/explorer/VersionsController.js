Ext.define('CmsConfigExplorer.view.explorer.VersionsController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.explorer-versions',
    
    onVerDblClick: function(v, record, tr, rowIndex, e, eOpts){
        
//        if(record.get("fit") == "cnf"){
            var vid = record.get("gid");

            //console.log('in fol cont, fwd event');
            //console.log(vid);
        
            var name = record.get("name");
            var names = name.split("/");
            var online = 'False';
            var x;

            if (names[1] == 'cdaq' || names[1] == 'minidaq'){
                online = 'True';
            }
        
            var view = this.getView();
            view.fireEvent('custOpenVer',vid,online);
//        }
    },
    
    onVerClick: function(v, record, tr, rowIndex, e, eOpts){
        
        var textA = this.lookupReference('descTextArea');
        textA.setValue(record.get("description"));
    }
    
});
