
Ext.define("Demo110315.view.sequence.Sequence",{
    extend: "Ext.panel.Panel",

    controller: "sequence-sequence",
    viewModel: {
        type: "sequence-sequence"
    },
    
    requires:['Demo110315.model.Sequenceitem'],
    
    alias:'widget.sequencetab',
    
    reference: "sequenceTab",

    layout: {
        type: 'border'
    },
    
//    listeners:{
//        custSetVerId: 'onSetVerId'
//    },
    
    items: [
        {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
                    {
                        xtype: 'textfield',
                        fieldLabel: 'Search',
                        labelWidth: 47,
                        enableKeyEvents: true,
                        disabled: true
                    }
                ]
        },
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'seqtree',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                rowclick: 'onSequenceNodeClick',
                custModParams: 'onSeqModParamsForward',
//                custPatDet: 'onPatDetForward',
                render: 'onSequenceRender',
                beforeshow: 'onSequenceRender'
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
            type:  'fit'
//            align: 'stretch'
        },
        
        items:[
//            {
//                xtype: 'container',
//                layout:{
//                    type: 'vbox',
//                    align: 'stretch'
//                },
//                items:[
//                    {
//                        xtype: 'seqmoduledetails',
//        //                width: '100%',
//                        height: '25%',
//                        title: 'Module Details',
//                        collapsible: true,
//                        split: true
//                    },
//                    {
//                        xtype: 'seqparameters',
//                        split: true,
//                        flex: 2,
//        //                layout: 'fit',
//                        loadMask: true,
//        //                width: '100%',
//                        height: '75%'
//                    }
//                    
//                ]
//                
//            }
//            ,{            
//                xtype: 'sequencedetails',
////                hidden: true,
//                split: true,
//                title: 'Sequence Details',
//                height: '100%'          
//            }
        ]
        
    }    
    ]
});
