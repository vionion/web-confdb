
Ext.define("CmsConfigExplorer.view.streamdataset.StreamTree",{
    extend: "Ext.tree.Panel",

    requires:['CmsConfigExplorer.view.streamdataset.StreamTreeController'],

    alias: 'widget.streamtree',

    controller: "streamdataset-streamtree",

    reference: "streamTree",

    bind:{
        store:'{streamitems}'
    },

    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 2,
        listeners: {
            beforeedit: 'onBeforeNodeEdit',
            edit: 'onNodeEditDone'
        }
    },
//    title: "Stream and Datasets",
    
    header: false,
    rootVisible: true,
    useArrows: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'strdatHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Stream & Dataset</b>'
            },
            {
                xtype: 'tbseparator'
            },
//            { 
//                xtype: 'button',
//                reference: 'abOrderButton',
//                text: 'Alphabetical Order',
//                listeners: {
//                    click: 'onAlphaOrderClick'
//                }
//            },
//            { 
//                xtype: 'button',
//                reference: 'origOrderButton',
//                text: 'Original Order',
//                disabled: true,
//                listeners: {
//                    click: 'onOrigOrderClick'
//                }
//            },
            {
                labelWidth: 120,
                xtype: 'textfield',
                fieldLabel: 'Stream search',
                reference: 'trigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'triggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onTriggerClick',
                        listeners: {
                            change: 'onSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'matches',
                fieldLabel: 'Matches',

                // Use shrinkwrap width for the label
                labelWidth: null,
                listeners: {
                    beforerender: function() {
                        var me = this,
                            tree = me.up('treepanel'),
                            root = tree.getRootNode(),
                            leafCount = 0;

                        tree.store.on('fillcomplete', function(store, node) {
                            if (node === root) {
                                root.visitPostOrder('', function(node) {
                                    if (node.isLeaf()) {
                                        leafCount++;
                                    }
                                });
                                me.setValue(leafCount);
                            }
                        });
                    },
                    single: true
                }
            }
        ]
    }],
    viewConfig: {
        plugins: [
            {
                pluginId: 'ds_drop_plugin',
                ptype: 'treeviewdragdrop',
                dragText: 'Drop path here to add to another dataset',
                dropGroup: 'path',
                enableDrag: false
            },
            {
                pluginId: 'event_move_plugin',
                ptype: 'treeviewdragdrop',
                dragText: 'Move this event config statements node to replace an existing one in another stream',
                dragGroup: 'event',
                dropGroup: 'event'
            }
        ],
        listeners: {
            beforedrop: 'beforeDrop'
        }
    },
    columns: [
        {
            xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1, sortable: false,
            editor: {
                xtype: 'textfield',
                selectOnFocus: true,
                editable: true
            }
        }

    ]
});
