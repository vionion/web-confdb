Ext.define('CmsConfigExplorer.view.module.ModuleGridController', {
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
    },
    
    onModTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('modtrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onModuleSearchChange: function( form, newValue, oldValue, eOpts ) {

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
                    
// 
//                    if (node.get('pit') == "pat"){
//                        
//                        visible = v.test(node.get('Name'));
//                        
//                        if(visible) {
//                            matches++;
//                        }
//                        
//                    }
//                    else if (node.isRoot()){
//                        
//                        visible = true;
//                    }
//                    else {
//  
//                        var found = false;
//                        var parent = node;
//                        
//                        while(!found){
//                            parent = parent.parentNode;
//                            if (parent.get('pit') == 'pat'){
//                                found = true;
//                            }
//                        }
//  
//                        visible = v.test(parent.get('Name'));
//                        
//                    }
                    
                    return visible;
                }

            });
            var mat = this.lookupReference('modMatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
});
