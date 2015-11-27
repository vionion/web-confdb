
Ext.define("CmsConfigExplorer.view.module.ModuleGrid",{
    extend: "Ext.grid.Panel",

    requires:['CmsConfigExplorer.view.module.ModuleGridController'],
    
    controller: "module-modulegrid",
    
    alias: 'widget.modulesgrid',

    listeners: {
        rowclick: 'onGridModuleClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{modules}',
        selection: '{selectedModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridModuleClick',
        scope: 'controller'    
    },
//    loadMask: true,
//    viewConfig: {
//        loadingHeight: 100
//    },
    reference: 'modulesGrid',
    
//    title: 'Configuration Modules',
    header: false,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'modHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Modules</b>'
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
                fieldLabel: 'Module search',
                reference: 'modtrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'modTriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onModTriggerClick',
                        listeners: {
                            change: 'onModuleSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onModuleSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'modMatches',
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
            xtype: 'gridcolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
//        {
//            xtype: 'gridcolumn',
//            text: 'ID',
//            flex: 1,
//            dataIndex: 'gid'
//
//        },
        {
            xtype: 'gridcolumn',
            text: 'Class',
            flex: 1,
            dataIndex: 'mclass'

        },
        {
            xtype: 'gridcolumn',
            text: 'Type',
            flex: 1,
            dataIndex: 'mt'

        }
    ]
});
