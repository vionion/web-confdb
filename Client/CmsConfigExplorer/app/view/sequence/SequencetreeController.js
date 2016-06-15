Ext.define('CmsConfigExplorer.view.sequence.SequencetreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.sequence-sequencetree',
    
    onSeqTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('seqtrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onSeqSearchChange: function( form, newValue, oldValue, eOpts ) {

        var tree = this.getView(),
            v = null,
            matches = 0;

        tree.store.clearFilter();

        try {
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
            tree.store.filter({
                filterFn: function(node) {
                    
                    if (!node.isRoot()){
                    
                        var children = node.childNodes,
                            len = children && children.length,
    //                        visible = node.isLeaf() ? v.test(node.get('name')) : false,
                            visible = (v.test(node.get('Name'))),
                            i;
//                        

                        for (i = 0; i < len && !(visible = children[i].get('visible')); i++);

    //                    if (visible && node.isLeaf()) {
                        if (visible) {
                            matches++;
                        }
                        
                        if (node.parentNode){
                            visible = (visible || v.test(node.parentNode.get('Name'))); 
                        }
                        
                        if (node.parentNode.parentNode){ // NOT SO NICE
                            visible = (visible || v.test(node.parentNode.parentNode.get('Name'))); // NOT SO NICE
                        }
                        
                        return visible;
                    }

                }

            });
            var mat = this.lookupReference('seqmatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    
});
