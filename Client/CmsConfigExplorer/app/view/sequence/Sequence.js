
Ext.define("CmsConfigExplorer.view.sequence.Sequence",{
    extend: "Ext.panel.Panel",

    controller: "sequence-sequence",
    viewModel: {
        type: "sequence-sequence"
    },

    listeners:{
        doSmthToAllNodes: 'doSmthToAllNodes'
    },
    
    requires:['CmsConfigExplorer.model.Sequenceitem'],
    
    alias:'widget.sequencetab',
    
    reference: "sequenceTab",

    layout: {
        type: 'border'
    },
    
    items: [
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'seqtree',
            height: '100%',
            loadMask: true,
            viewConfig: {
                loadingHeight: 100,
                plugins: {
                    ptype: 'treeviewdragdrop',
                    dragText: 'Drag and drop to reorganize'
                },
                listeners: {
                    beforedrop: 'beforedrop'
                }
            },
            listeners: {
                rowclick: 'onSequenceNodeClick',
                custModParams: 'onSeqModParamsForward',
//                custPatDet: 'onPatDetForward',
                render: 'onSequenceRender',
                beforeshow: 'onSequenceRender',
                onBeforeDrop: 'beforedrop',
                viewready: 'addBeforeDragListener'
                //scope: 'controller'
        }

    },
    {
        region: 'center',
        xtype: 'panel',
        reference: "centralPanel",
        header: false,
        split: true,
        height: '100%',
        
        layout:{
            type:  'vbox'
//            align: 'stretch'
        },
        
        items:[
                {
                    xtype: 'seqmoduledetails',
                    width: '100%',
                    height: '25%',
                    title: 'Module Details',
                    collapsible: true,
                    split: true
                },
                {
                    xtype: 'parameters',
                    split: true,
                    flex: 2,
    //                layout: 'fit',
                    loadMask: true,
                    width: '100%',
                    height: '75%'
                }

        ]
        
    }    
    ]
});
