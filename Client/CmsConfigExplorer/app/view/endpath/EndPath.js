
Ext.define("CmsConfigExplorer.view.endpath.EndPath",{
    extend: "Ext.panel.Panel",
    
    requires:['CmsConfigExplorer.view.endpath.EndPathController',
             "CmsConfigExplorer.view.endpath.EndPathDetails",
             'CmsConfigExplorer.view.endpath.EndPathModel',
             "CmsConfigExplorer.view.endpath.EndPathModuleDetails",
             'CmsConfigExplorer.view.param.Parameters',
             "CmsConfigExplorer.view.endpath.EndPathTree",
             "CmsConfigExplorer.view.endpath.EndPathSmartPrescale"],
    
    controller: "endpath-endpath",
    viewModel: {
        type: "endpath-endpath"
    },

    alias:'widget.endpathtab',
    
    reference: "endpathtab",
    
    layout: {
        type: 'border'
    },

    listeners:{
        doSmthToAllNodes: 'doSmthToAllNodes'
    },

    items: [
//        {
//            xtype: 'toolbar',
//            region: 'north',
//            paddingLeft: 5,
//            items:[ 
//                    {
//                        xtype: 'textfield',
//                        fieldLabel: 'Search',
//                        labelWidth: 47,
//                        enableKeyEvents: true,
//                        disabled: true
//                    }
//                ]
//        },
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'endpathtree',
            height: '100%',
    //        collapsible: true,
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
            listeners:{
                cusPathColumnNameHeaderClickForward: 'onPathColumnNameHeaderClickForward',
                rowclick: 'onEndNodeClick',
                cusEndModParams: 'onEndModParamsForward',
                cusEndOumModParams: 'onEndOumModParamsForward',
                cusAlphaOrderClickForward: 'onSortAlphaPaths',
                cusOrigOrderClickForward: 'onSortOriginalPaths',
//                custPatDet: 'onPatDetForward',
                render: 'onEndRender',
                beforeshow: 'onEndRender',
                onBeforeDrop: 'beforedrop',
                viewready: 'addBeforeDragListener'
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
                    reference: "endCentralContainer",
                    layout:{
                        type: 'vbox',
                        align: 'stretch'
                    },
                    items:[
                        {
                            xtype: 'endmoduledetails',
            //                width: '100%',
//                            maxHeight: '25%',
                            title: 'Module Details',
                            collapsible: true,
                            flex: 1,
                            split: true,
                            listeners:{
                                cusSmartPrescale: 'onSmartPrescaleClick',
                                cusNotSmartPrescale: 'onNotSmartPrescaleClick'
                            }
                        },
                        {
                            xtype: 'parameters',
                            split: true,
                            flex: 3,
            //                layout: 'fit',
                            loadMask: true
            //                width: '100%',
//                            maxHeight: '75%'
                        },
                        {
                            xtype: 'endpathsmartprescale',
//                            reference: 'endSpGrid',
                            split: true,
                            flex: 1,
                            collapsible: true,
//                            maxHeight: '25%',
                            collapseDirection : 'bottom',
//                            hidden: true,
                            listeners:{
                                cusOnEpsSearchChange: 'onFwdEpsSearchChange'
                            }
                            
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
