
Ext.define("CmsConfigExplorer.view.path.Pathtree",{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.path.PathtreeController'],
    
    alias: 'widget.pathtree',
    
    controller: "path-pathtree",
    
//    reference: "pathTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{pathitems}'
//        selection: '{selectedPathitem}'
    },
    
//    title: "Paths",
    header: false,
    rootVisible: true,
    useArrows: true,
//    singleExpand: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'pathHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Paths</b>'
            },
            {
                xtype: 'tbseparator'
            },
            { 
                xtype: 'button',
                reference: 'abOrderButton',
                text: 'Alphabetical Order',
                listeners: {
                    click: 'onAlphaOrderClick'
                }
            },
            { 
                xtype: 'button',
                reference: 'origOrderButton',
                text: 'Original Order',
                disabled: true,
                listeners: {
                    click: 'onOrigOrderClick'
                }
            },
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
    
    columns: [
        { xtype: 'treecolumn', 
            header: 'Name', 
            dataIndex: 'Name', 
            flex: 1, 
            sortable: false
//            listeners:
//                {
//                    headerclick: 'onPathColumnNameHeaderClick'
//                }
            
        }
    ]
    
});
