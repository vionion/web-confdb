
Ext.define("CmsConfigExplorer.view.essource.ESSourceGrid",{
    extend: "Ext.tree.Panel",

    requires:['CmsConfigExplorer.view.essource.ESSourceGridController'],
    
    controller: "essource-essourcegrid",

    alias: 'widget.essourcegrid',

    listeners: {
        rowclick: 'onGridESSourceClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{essource}'
//        ,selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridESSourceClick',
        scope: 'controller'    
    },
//    viewConfig: {
//        loadingHeight: 100
//    },
    loadMask: true,
    
    reference: 'esSourceGrid',
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'modHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>ES Source</b>'
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
                labelWidth: 130,
                xtype: 'textfield',
                fieldLabel: 'ES Source search',
                reference: 'esstrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'essTriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onEssTriggerClick',
                        listeners: {
                            change: 'onESSourceSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onESSourceSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'essrcMatches',
                fieldLabel: 'Matches',

                // Use shrinkwrap width for the label
                labelWidth: null
//                ,listeners: {
//                    beforerender: function() {
//                        var me = this,
//                            tree = me.up('gridpanel'),
//                            root = tree.getRootNode(),
//                            leafCount = 0;
//
//                        tree.store.on('fillcomplete', function(store, node) {
//                            if (node === root) {
//                                root.visitPostOrder('', function(node) {
//                                    if (node.isLeaf()) {
//                                        leafCount++;
//                                    }
//                                });
//                                me.setValue(leafCount);
//                            }
//                        });
//                    },
//                    single: true
//                }
            }
        ]
    }],
    
    header: false,
    useArrows: true,
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
        {
            xtype: 'gridcolumn',
            text: 'Class',
            flex: 2,
            dataIndex: 'tclass'
        }
    ]
});
