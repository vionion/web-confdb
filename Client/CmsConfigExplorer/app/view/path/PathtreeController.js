Ext.define('CmsConfigExplorer.view.path.PathtreeController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.path-pathtree',
    
    onModuleClick: function( v, record, tr, rowIndex, e, eOpts) {
        
        var item_type = record.get("pit");
        
        if(item_type == "mod"){
            var mid = record.get("internal_id");
            var pid = record.get("id_pathid");

            //console.log('in child, fwd event');
            //console.log(mid);
            var view = this.getView();
            view.fireEvent('custModParams',mid, pid);
        }

        else  if(item_type == "pat"){
            var pid = record.get("gid");

            //console.log('in child, fwd event');
            //console.log(mid);
            var view = this.getView();
            view.fireEvent('custPatDet', pid);
        }
//        else if((item_type == "pat") || (item_type == "seq")){
//            
//            this.lookupReference('pathTree').expandNode( record, false);
//        }
        
    },
    
    onPathColumnNameHeaderClick: function(ct, column, e, t, eOpts){
        
//        var view = this.getView();
//        view.fireEvent('cusPathColumnNameHeaderClickForward', ct, column, e, t, eOpts);
    },
    
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
 
                    if (node.get('pit') == "pat"){
                        
                        visible = v.test(node.get('Name'));
                        
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
                            if (parent.get('pit') == 'pat'){
                                found = true;
                            }
                        }
  
                        visible = v.test(parent.get('Name'));
                        
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

    beforedrop: function (node, data, overModel, dropPosition, dropHandler) {
        var view = this.getView();
        view.fireEvent('onBeforeDrop', node, data, overModel, dropPosition, dropHandler);
    }

});
