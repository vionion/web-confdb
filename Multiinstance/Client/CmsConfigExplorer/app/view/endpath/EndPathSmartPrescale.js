
Ext.define("CmsConfigExplorer.view.endpath.EndPathSmartPrescale",{
    extend: "Ext.grid.Panel",
 
    requires: [
        "CmsConfigExplorer.view.endpath.EndPathSmartPrescaleController"
        ,"CmsConfigExplorer.view.endpath.EndPathSmartPrescaleModel"
    ],
    
    controller: "endpath-endpathsmartprescale",
    viewModel: {
        type: "endpath-endpathsmartprescale"
    },
    
//    bind:{
//        // bind store to view model "modules" store
//        store:'{endspexpressions}'
//    },
    
    alias: "widget.endpathsmartprescale",
    reference: 'endSpGrid',
    autoScroll: true,
    bufferedRenderer: false,
    
    bind: {
        title: '{spname} expressions',
        store: '{endspexpressions}'
    },
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'endPathSmartPrescaleTooolBar',
        dock: 'top',

        items: [


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
                fieldLabel: 'expression Path search',
                reference: 'epstrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'epstriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onEspTriggerClick',
                        listeners: {
                            change: 'onEpsSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onEpsSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'epsmatches',
                fieldLabel: 'Matches',

                // Use shrinkwrap width for the label
                labelWidth: null
//                listeners: {
//                    render: function() {
//                        var me = this,
//                            tree = me.up('grid'),
////                            root = tree.getRootNode(),
//                            leafCount = 0;
//                        
//                        console.log(tree.store);
//                        console.log("HERE");
//
////                        tree.store.on('fillcomplete', function(store, node) {
//////                            if (node === root) {
//////                                root.visitPostOrder('', function(node) {
//////                                    if (node.isLeaf()) {
//////                                        leafCount++;
//////                                    }
//////                                });
//////                                me.setValue(leafCount);
//////                            }
////                            
////                            
////                            
////                        });
//                    }
////                    ,single: false
//                }
            }
        ]
    }],
    
    columns: [

        { xtype: 'gridcolumn', header: 'Path', dataIndex: 'path', flex: 3},
        { xtype: 'gridcolumn', header: 'Smart Prescale', dataIndex: 'smprescale', flex: 1}
    ]
});
