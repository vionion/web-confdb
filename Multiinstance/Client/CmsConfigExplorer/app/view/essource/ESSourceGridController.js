Ext.define('CmsConfigExplorer.view.essource.ESSourceGridController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.essource-essourcegrid',
    
        onGridESSourceClick: function( v, record, tr, rowIndex, e, eOpts) {
    
        var mid = record.get("gid");
        var view = this.getView();
        view.fireEvent('custGridESSourceParams',mid);
    }
   
    ,onEssTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('esstrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    }
    
    
    ,onESSourceSearchChange: function( form, newValue, oldValue, eOpts ) {

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
            var mat = this.lookupReference('essrcMatches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    
    
});
