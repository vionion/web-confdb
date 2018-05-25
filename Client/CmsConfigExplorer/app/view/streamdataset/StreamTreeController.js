Ext.define('CmsConfigExplorer.view.streamdataset.StreamTreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-streamtree',
    
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
 
                    if (node.get('s_type') == "str"){
                        
                        visible = v.test(node.get('name'));
                        
                        if(visible) {
                            matches++;
                        }
                        
                    }
                    else if (node.isRoot()){
                        
                        visible = true;
                    }
                    else {
  
                        var found = false;
                        var parent = node;
                        
                        while(!found){
                            parent = parent.parentNode;
                            if (parent.get('s_type') == 'str'){
                                found = true;
                            }
                        }
  
                        visible = v.test(parent.get('name'));
                        
                    }
                    
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
    },

    onBeforeNodeEdit: function (editor, context, eOpts) {
        if (context.record.data.s_type === 'evc') {
            return true;
        } else {
            return false;
        }
    },

    onNodeEditDone: function (editor, context, eOpts) {
        console.log('done');
        // TODO: send request about node name change, receive new internal_id and update node
    }
});
