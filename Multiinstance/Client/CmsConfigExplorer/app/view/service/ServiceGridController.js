Ext.define('CmsConfigExplorer.view.service.ServiceGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.service-servicegrid',
    
    onSrvTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('srvtrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onServiceSearchChange: function( form, newValue, oldValue, eOpts ) {

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
            var mat = this.lookupReference('srvMatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    
});
