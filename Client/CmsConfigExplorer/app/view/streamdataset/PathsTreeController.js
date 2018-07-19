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
    },

    onEditDataset: function () {
        var datasetPaths = this.getViewModel().getStore('datasetpaths');
        var streamsDatasetTab = this.getView().up().up();
        var pathTab = streamsDatasetTab.prev().prev().prev().prev().prev().prev();
        var allPaths = pathTab.getViewModel().getStore('pathitems');
        var allPathsFilteredCopy =  new Ext.data.Store({model: allPaths.model});
        allPaths.each(function(r){
            allPathsFilteredCopy.add(r.copy());
        });
        allPathsFilteredCopy.filter('pit', 'pat');
        var selected = [];
        datasetPaths.each(function (rec) {
                selected.push(rec.data.internal_id);
            }
        );
        var datasetpaths_store = this.getViewModel().getStore('datasetpaths');
        var version = this.getViewModel().get("idVer");
        var win = new Ext.Window({
            layout: 'border', width: "75%",
            height: 460, closeAction: 'hide', buttonAlign: 'center',
            animShow: function () {
                this.el.slideIn('t', {
                    duration: 1, callback: function () {
                        this.afterShow(true);
                    }, scope: this
                });
            },
            animHide: function () {
                this.el.disableShadow();
                this.el.slideOut('t', {
                    duration: 1, callback: function () {
                        this.el.hide();
                        this.afterHide();
                    }, scope: this
                });
            },
            items: [{
                xtype: 'itemselectorfield',
                name: 'Features',
                region: 'center',
                padding: 20,
                store: allPathsFilteredCopy,
                displayField: 'Name',
                valueField: 'internal_id',
                value: selected,
                allowBlank: true,
                fromTitle: 'Available',
                toTitle: 'Selected',
                buttons: ['add', 'remove'],
                delimiter: undefined
            }],
            dockedItems: [{
                xtype: 'toolbar',
                dock: 'bottom',
                ui: 'footer',
                defaults: {
                    minWidth: 75
                },
                items: [{
                    text: 'Save',
                    handler: function () {
                        var selector = this.up().up().items.items[0];
                        if (selector.isValid()) {
                            // please, replace such stupid code pieces
                            var datasetId = streamsDatasetTab.lookupReference('streamTree').getSelectionModel().getSelection()[0].data.internal_id;
                            var pathIds = selector.value;
                            var requestObj = {
                                'datasetId': datasetId,
                                'pathIds': pathIds,
                                'version': version
                            };
                            Ext.Ajax.request({
                                url: 'dataset_update',
                                method: 'POST',
                                headers: {'Content-Type': 'application/json'},
                                jsonData: JSON.stringify(requestObj),
                                failure: function (response) {
                                    Ext.Msg.alert('Error', response.responseText);
                                    console.log(response);
                                }, success: function (response) {
                                    // if (response.status == 200) {
                                    datasetpaths_store.reload();
                                    win.hide();
                                    // }
                                }
                            });

                        }
                    }
                },
                    {
                        text: 'Close',
                        handler: function () {
                            win.hide();
                        }
                    }]
            }]
        });


        win.show(Ext.getBody());
    }

});
