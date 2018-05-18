
Ext.define("CmsConfigExplorer.view.path.Path",{
    extend: "Ext.panel.Panel",

    requires:['CmsConfigExplorer.view.param.Parameters',
             'CmsConfigExplorer.view.path.Pathtree',
             'CmsConfigExplorer.view.path.ModuleDetails',
             'CmsConfigExplorer.view.path.PathDetails',
             'CmsConfigExplorer.view.path.PathController',
              'CmsConfigExplorer.view.path.PathModel'
             ],

    alias:'widget.pathtab',

    reference: "pathtab",

    controller: "path-path",
    viewModel: {
        type: "path-path"
    },

    listeners:{
        cusDetailsClick: 'onDetailsRender',
        scope: 'controller',
        doSmthToAllNodes: 'doSmthToAllNodes'
    }

    ,layout: {
        type: 'border'
    },
    height: '100%',
//    listeners:{
//        custSetVerId: 'onSetVerId'
//    },

    items: [
//        {
//            xtype: 'toolbar',
//            region: 'north',
//            paddingLeft: 5,
//            border: '0 0 1 0',
//            items:[ 
//                    {
//                        xtype: 'textfield',
//                        fieldLabel: 'Search',
//                        labelWidth: 47,
//                        enableKeyEvents: true,
//                        disabled: true
//                    }
////                    ,{
////                        
////                        text: 'Sort by Name',
////                        handler : 'onPathColumnNameHeaderClickForward',
////                        scope: 'controller'
////                    }
//                ]
//        },
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'pathtree',
            reference: "pathTree",
            height: '100%',
    //        collapsible: true,
//            loadMask: true,
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
                rowclick: 'onNodeClick',
                custModParams: 'onModParamsForward',
                cusAlphaOrderClickForward: 'onSortAlphaPaths',
                cusOrigOrderClickForward: 'onSortOriginalPaths',
                onBeforeDrop: 'beforedrop',
                viewready: 'addBeforeDragListener'
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
                        xtype: 'moduledetails',
        //                width: '100%',
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
        //                width: '100%',
                        height: '75%'
                    }

                ]

            },
            {
                xtype: 'pathdetails',
//                hidden: true,
                split: true,
                title: 'Path Details',
                height: '100%'
            }
        ]

    }
    ]

});

