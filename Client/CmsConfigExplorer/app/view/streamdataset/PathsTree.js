
Ext.define("CmsConfigExplorer.view.streamdataset.PathsTree",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.streamdataset.PathsTreeController'],
    
    controller: "streamdataset-pathstree",
    
    alias: 'widget.datasetpaths',
    
    reference: "datasetPathsTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{datasetpaths}'

    },
    header: false,
//    title: "Paths",
    rootVisible: false,
    useArrows: true,
    scrollable: true,
    bufferedRenderer: false,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'pathHeaderTooolBar',
        dock: 'top',

        items: [
            {
                text: 'Edit',
                listeners: {
                    click: 'onEditDataset',
                    scope: 'controller'
                }
            },
            { 
                xtype: 'tbtext',
                bind: {
                    text: '<b>{current_dat} Paths</b>'
                }
                
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
                labelWidth: 80,
                xtype: 'textfield',
                fieldLabel: 'Path search',
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
        plugins: {
            ptype: 'treeviewdragdrop',
            dragText: 'Drag path to another dataset',
            dragGroup: 'path',
            enableDrop: false
        }
    },
    columns: [
        {xtype: 'treecolumn', header: 'Name', dataIndex: 'name', flex: 1, sortable: true}

    ]
});
