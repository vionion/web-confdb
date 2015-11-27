
Ext.define("CmsConfigExplorer.view.edsource.EDSourceGrid",{
    extend: "Ext.tree.Panel",

    requires:['CmsConfigExplorer.view.edsource.EDSourceGridController'],
    
    controller: "edsource-edsourcegrid",

    alias: 'widget.edsourcegrid',

    listeners: {
        rowclick: 'onGridEDSourceClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{edsource}'
//        ,selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridEDSourceClick',
        scope: 'controller'    
    },
    loadMask: true,
    
    reference: 'edSourceGrid',
    
//    title: 'Configuration ED Source',
    header: false,
    
    useArrows: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'edSourceHeaderTooolBar',
        dock: 'top',
        minHeight : 40,

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>ED Sources</b>'
            }
//            ,{
//                xtype: 'tbseparator'
//            },
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
//            {
//                labelWidth: 120,
//                xtype: 'textfield',
//                fieldLabel: 'ED Source search',
//                reference: 'trigfield',
////                triggerWrapCls: 'x-form-clear-trigger',
//                triggers:{
//                    search: {
//                        reference: 'triggerSearch',
//                        cls: 'x-form-clear-trigger',
//                        handler: 'onTriggerClick',
//                        listeners: {
//                            change: 'onSearchChange'
//
//                        }
//                    }
//                }, 
//                listeners: {
//                    change: 'onSearchChange'
//                    
//                }
//            }
//            ,{
//                xtype: 'displayfield',
//                reference: 'matches',
//                fieldLabel: 'Matches',
//
//                // Use shrinkwrap width for the label
//                labelWidth: null,
//                listeners: {
//                    beforerender: function() {
//                        var me = this,
//                            tree = me.up('treepanel'),
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
//            }
        ]
    }],
    
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
