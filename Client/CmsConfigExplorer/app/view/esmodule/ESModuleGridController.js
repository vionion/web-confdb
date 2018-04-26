Ext.define('CmsConfigExplorer.view.esmodule.ESModuleGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.esmodule-esmodulegrid',
    
    onGridESModuleClick: function( v, record, tr, rowIndex, e, eOpts) {
        
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
    
        var mid = record.get("internal_id");
        var view = this.getView();
        view.fireEvent('custGridESModParams',mid);
    }
    
    ,onEsModTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('esmodtrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    }
    
    ,onESModuleSearchChange: function( form, newValue, oldValue, eOpts ) {

        var tree = this.getView(),
            v = null,
            matches = 0;

        tree.store.clearFilter();

        try {
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
            tree.store.filter({
                filterFn: function(record) {
                    
                    var visible = true;
                    
                    visible = v.test(record.get('name'));
                    
                    if(visible) {
                            matches++;
                    }
                                        
                    return visible;
                }

            });
            var mat = this.lookupReference('esmodMatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
});
