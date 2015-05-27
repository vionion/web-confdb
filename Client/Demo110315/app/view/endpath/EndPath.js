
Ext.define("Demo110315.view.endpath.EndPath",{
    extend: "Ext.panel.Panel",

    controller: "endpath-endpath",
    viewModel: {
        type: "endpath-endpath"
    },

    alias:'widget.endpathtab',
    
    reference: "endpathtab",
    
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
            xtype: 'endpathtree',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                rowclick: 'onEndNodeClick',
                cusEndModParams: 'onEndModParamsForward',
                cusEndOumModParams: 'onEndOumModParamsForward',
//                custPatDet: 'onPatDetForward',
                render: 'onEndRender',
                beforeshow: 'onEndRender'
                //scope: 'controller'
            }

        },
        {
            region: 'center',
            xtype: 'panel',
            reference: "endCentralPanel",
            header: false,
            split: true,
            height: '100%',

            layout:{
                type:  'card'
    //            align: 'stretch'
            },

            items:[
                {
                    xtype: 'container',
                    layout:{
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items:[
                        {
                            xtype: 'endmoduledetails',
            //                width: '100%',
                            height: '25%',
                            title: 'Module Details',
                            collapsible: true,
                            split: true
                        },
                        {
                            xtype: 'endparameters',
                            split: true,
                            flex: 2,
            //                layout: 'fit',
                            loadMask: true,
            //                width: '100%',
                            height: '75%'
                        }

                    ]

                }
                ,{            
                    xtype: 'endpathdetails',
    //                hidden: true,
                    split: true,
                    title: 'End Path Details',
                    height: '100%'          
                }
            ]

        }    
    ]
    
});
