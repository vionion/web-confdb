
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
        scope: 'controller'
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
                    beforedrop: function( node, data, overModel, dropPosition, dropHandler){
                        if ((dropPosition !== 'append') && (overModel.parentNode.data.root)) {
                            dropHandler.cancelDrop();
                        }
                    },
                    drop: function (node, data, overModel, dropPosition) {
                        console.log(overModel);
                        console.log(dropPosition);
                        // I came to CERN to create a new order!
                        var newOrder;
                        var newParent;
                        if (dropPosition === 'append') {
                            newParent = overModel.data.Name;
                            // this is not working with paths, because they don't have children field. Must be fixed.
                            newOrder = overModel.data.children[overModel.data.children.length - 1].order;
                        } else if (dropPosition === 'before') {
                            newParent = overModel.parentNode.data.Name;
                            newOrder = overModel.data.order - 1;
                        } else if (dropPosition === 'after') {
                            newParent = overModel.parentNode.data.Name;
                            newOrder = overModel.data.order;
                        }
                        console.log('new parent: ' + newParent);
                        console.log('new order: ' + newOrder);
                        console.log('Drop!');
                    }
                }
            },
            listeners:{
                cusPathColumnNameHeaderClickForward: 'onPathColumnNameHeaderClickForward',
                rowclick: 'onNodeClick',
                custModParams: 'onModParamsForward',
                cusAlphaOrderClickForward: 'onSortAlphaPaths',
                cusOrigOrderClickForward: 'onSortOriginalPaths',
//                custPatDet: 'onPatDetForward',
//                render: 'onRender',
//                beforeshow: 'onRender'
                //scope: 'controller'
                viewready: function (tree) {
                    var view = tree.getView(),
                        dd = view.findPlugin('treeviewdragdrop');

                    dd.dragZone.onBeforeDrag = function (data, e) {
                        var rec = view.getRecord(e.getTarget(view.itemSelector));
                        console.log('old order: ' + rec.data.order);
                        // console.log(rec.parentNode.data.gid);
                        console.log('old parent: ' + rec.parentNode.data.Name);
                        // console.log(rec);
                        console.log('Drag!');
                        return true;
                    };
                }
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





//{
//        region: 'center',
//        collapsible: true,
//        xtype: 'moduledetails',
//        width: '100%',
//        height: '25%'
//    },{
//        region: 'south',
////        layout: 'fit',
//        xtype: 'parameters',
//        split: true,
//        height: '100%',
//        width: '50%',
//        loadMask: true
//        
//    }
