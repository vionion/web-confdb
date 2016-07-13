Ext.define('CmsConfigExplorer.view.endpath.EndPathSmartPrescaleController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.endpath-endpathsmartprescale',
    
    onEspTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('epstrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onEpsSearchChange: function( form, newValue, oldValue, eOpts ) {
        
        
//        this.getView().fireEvent("cusOnEpsSearchChange", form, newValue, oldValue, eOpts );
        
        var tree = this.getView(),
            store = this.getViewModel().getStore('endspexpressions'),
            v = null,
            matches = 0;
        
//        tree.store.clearFilter();
        store.clearFilter();
        
        try {
            v = new RegExp(form.getValue(), 'i');
            Ext.suspendLayouts();
//            tree.store.filter({
            store.filter({
                filterFn: function(node) {
                    
                    var visible = true;    

                    visible = v.test(node.get('path'));

                    if(visible) {
                        matches++;
                    }

                    return visible;
                }

            });
            var mat = this.lookupReference('epsmatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
//    ,onEndspexpressionsFilterChange: function( store, filters, eOpts ){
//        
//        var label = this.lookupReference('epsmatches');
//        label.setValue(store.getCount()); 
//        
//    }
    
    ,onEndspexpressionsLoad: function(store, records, successful, operation, node, eOpts){
    
        var label = this.lookupReference('epsmatches');
        label.setValue(records.length); 
        
    }
    
    
});
