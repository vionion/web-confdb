Ext.define('CmsConfigExplorer.view.streamdataset.PathsTreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-pathstree',
    
    onTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('trigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onSearchChange: function( form, newValue, oldValue, eOpts ) {

        var tree = this.getView(),
            v = null,
            matches = 0;

        tree.store.clearFilter();

        try {
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
            tree.store.filter({
                filterFn: function(node) {
                    
                    var visible = true;    
 
//                    if (node.get('pit') == "pat"){
                        
                    visible = v.test(node.get('name'));

                    if(visible) {
                        matches++;
                    }
                        
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
            var mat = this.lookupReference('matches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
});
