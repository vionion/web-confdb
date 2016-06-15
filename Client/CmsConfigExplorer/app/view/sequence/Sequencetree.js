
Ext.define("CmsConfigExplorer.view.sequence.Sequencetree",{
    extend: "Ext.tree.Panel",

    controller: "sequence-sequencetree",

    alias: 'widget.seqtree',
    
    reference: "seqTree",
    
    bind:{
        // bind store to view model "modules" store
        store:'{seqitems}'
    },
    
    header: false,
    rootVisible: true,
    useArrows: true,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'seqHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>Sequences</b>'
            },
            {
                xtype: 'tbseparator'
            },

            {
                labelWidth: 110,
                xtype: 'textfield',
                fieldLabel: 'Sequence search',
                reference: 'seqtrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'seqTriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onSeqTriggerClick',
                        listeners: {
                            change: 'onSeqSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onSeqSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'seqmatches',
                fieldLabel: 'Matches',

                // Use shrinkwrap width for the label
                labelWidth: null
            }
        ]
    }],
    
    columns: [
        { xtype: 'treecolumn', 
         header: 'Name', 
         dataIndex: 'Name', 
         flex: 1,
         sortable:false
        }

    ]
});
