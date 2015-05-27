Ext.define('Demo110315.view.module.ModuleGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.module-modulegrid',
    
    onGridModuleClick: function( v, record, tr, rowIndex, e, eOpts) {
        
//        var item_type = record.get("pit");
//        
//        if(item_type == "mod"){
//            var mid = record.get("gid");
//            var pid = record.get("id_pathid");
//
//            console.log('in child, fwd event');
//            console.log(mid);
//            var view = this.getView();
//            view.fireEvent('custModParams',mid, pid);
//        }
    
        var mid = record.get("gid");
        var view = this.getView();
        view.fireEvent('custGridModParams',mid);
    }
});
