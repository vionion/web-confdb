
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
                copyDroppedRecord: function (record) {
                    // Record from the grid. Take a copy ourselves
                    // because the built-in copying messes it up.
                    var copy = record.copy();
                    copy.id = Ext.id();
                    record.eachChild(function (child) {
                        copy.appendChild(this.copyDroppedRecord(child));
                    }, this);
                    return copy;

                },
                sendDnDrequest: function (nodeId, oldParent, newParent, order, copied) {
                    // Can be replased with just GET with params. It doesn't need to be more complicated than it can be
                    var dnRequestObj = {
                        'nodeId': nodeId,
                        'oldParent': oldParent,
                        'newParent': newParent,
                        'order': order,
                        'copied': copied
                    };
                    Ext.Ajax.request({
                        url: 'drag_n_drop',
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        jsonData: JSON.stringify(dnRequestObj),
                        // sucess: function (response) {
                        //     var obj = Ext.decode(response.responseText);
                        //     console.log(obj);
                        // },
                        failure: function (response) {
                            Ext.Msg.alert("Error");
                            console.log(response);
                        }
                    });
                },
                listeners: {
                    beforedrop: function (node, data, overModel, dropPosition, dropHandler) {
                        if ((dropPosition !== 'append') && (overModel.parentNode.data.root)) {
                            dropHandler.cancelDrop();
                        }

                        var oldParent = data.parent_internal_id;
                        var nodeId = data.records[0].data.internal_id;

                        // I came to CERN to create a new order!
                        var newOrder;
                        var newParent;
                        if (dropPosition === 'append') {
                            newParent = overModel.data.internal_id;
                            // this is not working with paths, because they don't have children field. Must be fixed.
                            newOrder = overModel.data.children[overModel.data.children.length - 1].order + 1;
                        } else if (dropPosition === 'before') {
                            newParent = overModel.parentNode.data.internal_id;
                            newOrder = overModel.data.order;
                        } else if (dropPosition === 'after') {
                            newParent = overModel.parentNode.data.internal_id;
                            newOrder = overModel.data.order + 1;
                        }
                        var copy = data.event.altKey;
                        if (copy) {
                            data.records = [this.copyDroppedRecord(data.records[0])];
                        }
                        this.sendDnDrequest(nodeId, oldParent, newParent, newOrder, copy);
                        dropHandler.processDrop();
                    }
                }
            },
            listeners:{
                cusPathColumnNameHeaderClickForward: 'onPathColumnNameHeaderClickForward',
                rowclick: 'onNodeClick',
                custModParams: 'onModParamsForward',
                cusAlphaOrderClickForward: 'onSortAlphaPaths',
                cusOrigOrderClickForward: 'onSortOriginalPaths',
                viewready: function (tree) {
                    var view = tree.getView(),
                        dz = view.findPlugin('treeviewdragdrop');
                    dz.dragZone.onBeforeDrag = function (data, e) {
                        var rec = view.getRecord(e.getTarget(view.itemSelector));
                        data.parent_internal_id = rec.parentNode.data.internal_id;
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

