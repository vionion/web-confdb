
Ext.define('CmsConfigExplorer.view.globalpset.GlobalPsetTree',{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.globalpset.GlobalPsetTreeController'],
    
    alias: 'widget.gpsettree',
    reference: 'gpsetTree',
    
    controller: "globalpset-globalpsettree",

    bind:{
        // bind store to view model "modules" store
        store:'{gpsets}'
//        selection: '{selectedService}'
 
    },
    
//    title: 'Global Parameter Sets',
    header: false,
    useArrows: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'gpsetHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Global PSets</b>'
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
                labelWidth: 140,
                xtype: 'textfield',
                fieldLabel: 'Global PSets search',
                reference: 'gpsettrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'triggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onTriggerClick',
                        listeners: {
                            change: 'onGpsetSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onGpsetSearchChange'

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
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
        { 
            xtype: 'gridcolumn', 
            header: 'Tracked', 
            dataIndex: 'tracked',
            sortable: false,
            renderer: function(v, meta, rec) 
                                {   var  data = rec.getData(); 
                                    if (data.tracked == 1)
                                        {return "tracked"} 
                                    else {return "untracked"} 
                                }
        }
    ]
});
