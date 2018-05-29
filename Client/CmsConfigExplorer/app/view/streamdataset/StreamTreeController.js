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
        var evcoNamesEditor = new Ext.grid.plugin.CellEditing({
            xtype: 'combo',
            queryMode: 'local',
            autoLoad: false,
            // to allow freetype
            forceSelection: false,
            hideTrigger: true,
            typeAhead: true,
            store: evcoNames,
            displayField: 'name'
        });
        if (context.record.data.s_type === 'evc') {
            context.column.setEditor(evcoNamesEditor);
            return true;
        } else {
            return false;
        }
    },

    onNodeEditDone: function (editor, context, eOpts) {
        var modified = false;
        if (context.record.modified && context.record.modified.name) {
            modified = true;
        }
        if (modified) {
            var evcon_replace = {
                'stream_id': context.record.parentNode.data.internal_id,
                'version_id': this.getViewModel().get("idVer")
            };
            var evcon = evcoNames.findRecord('name', context.value);
            if (!evcon) {
                evcon_replace['value'] = context.value;
                evcon_replace['internal_evcon_id'] = -1;
            } else {
                evcon_replace['internal_evcon_id'] = evcon.data.internal_id;
            }
            Ext.Ajax.request({
                url: 'update_streams_event',
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                jsonData: JSON.stringify(evcon_replace),
                failure: function (response) {
                    Ext.Msg.alert("Error");
                    console.log(response);
                },
                success: function (response) {
                    console.log(response.responseText);
                }
            });
        }
    },

    beforePathDrop: function (node, data, overModel, dropPosition, dropHandler) {
        if (overModel.data.s_type === 'dat') {
            console.log('append this path to dataset with id ' + overModel.data.internal_id);
                        var nodeId = data.records[0].data.internal_id;
            console.log('pathId is id ' + nodeId);
        }
        dropHandler.cancelDrop();
    },

    afterRender: function (tree) {
        var view = tree.getView(),
            plugin = view.findPlugin('treeviewdragdrop');
        plugin.dropZone.onNodeOver = function (node, dragZone, e, data) {
            var me = this;

            var element = Ext.fly(node);
            if (e.getTarget(view.itemSelector) !== null) {
                var rec = view.getRecord(e.getTarget(view.itemSelector));
                if (!element || (element && !(rec.data.s_type === 'dat'))) {
                    me.invalidateDrop();
                    return me.dropNotAllowed;
                } else if (me.valid) {
                    me.getIndicator().show();
                }
            } else {
                me.invalidateDrop();
                return me.dropNotAllowed;
            }

            if (!Ext.Array.contains(data.records, me.view.getRecord(node))) {
                me.positionIndicator(node, data, e);
            }

            return me.valid ? me.dropAllowed : me.dropNotAllowed;
        }
    }

});
