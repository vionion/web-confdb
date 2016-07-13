Ext.define('CmsConfigExplorer.view.globalpset.GlobalPsetTreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.globalpset-globalpsettree',
    
    onAlphaOrderClick: function(){
        var view = this.getView();
        view.fireEvent('cusAlphaOrderClickForward');
    },
    
    onOrigOrderClick: function(){
        var view = this.getView();
        view.fireEvent('cusOrigOrderClickForward');
    },
    
    onTriggerClick: function() {
        // Will trigger the change listener
        var tf = this.lookupReference('gpsettrigfield');
//        var t = tf.lookupReference('triggerSearch');
        tf.reset();
    },
    
    onGpsetSearchChange: function( form, newValue, oldValue, eOpts ) {

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
                    
//                    var visible = true;    
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
            var mat = this.lookupReference('matches');
            mat.setValue(matches);
            
            Ext.resumeLayouts(true);
            
        } catch (e) {
            form.markInvalid('Invalid regular expression');
            console.log(e);
        }
    }
    
    
});
