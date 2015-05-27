Ext.define('Demo110315.view.path.PathtreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-pathtree',
    
    onModuleClick: function( v, record, tr, rowIndex, e, eOpts) {
        
        var item_type = record.get("pit");
        
        if(item_type == "mod"){
            var mid = record.get("gid");
            var pid = record.get("id_pathid");

            console.log('in child, fwd event');
            console.log(mid);
            var view = this.getView();
            view.fireEvent('custModParams',mid, pid);
        }
        
        else  if(item_type == "pat"){
            var pid = record.get("gid");

            console.log('in child, fwd event');
            console.log(mid);
            var view = this.getView();
            view.fireEvent('custPatDet', pid);
        }
//        else if((item_type == "pat") || (item_type == "seq")){
//            
//            this.lookupReference('pathTree').expandNode( record, false);
//        }
        
    }
    
});
