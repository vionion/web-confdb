
Ext.define("CmsConfigExplorer.view.service.ServiceGrid",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.service.ServiceGridController'],
    
    alias: 'widget.servicesgrid',
    reference: 'servicesGrid',
    
    controller: "service-servicegrid",

//    listeners: {
//        rowclick: 'onGridServiceClick',
//        scope: 'controller'    
//    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{services}',
        selection: '{selectedService}'
 
    },
    
//    title: 'Configuration Services',
    header: false,
    useArrows: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'srvHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Services</b>'
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
                labelWidth: 150,
                xtype: 'textfield',
                fieldLabel: 'Service search',
                reference: 'srvtrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'srvTriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onSrvTriggerClick',
                        listeners: {
                            change: 'onServiceSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onServiceSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'srvMatches',
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
    
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        }
    ]
});
