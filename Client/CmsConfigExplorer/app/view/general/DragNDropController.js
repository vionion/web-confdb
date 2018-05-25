Ext.define('CmsConfigExplorer.view.general.DragNDropController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.general-dragNdrop',

    beforedrop: function (node, data, overModel, dropPosition, dropHandler) {
        if ((dropPosition !== 'append') && (overModel.parentNode.data.root)) {
            dropHandler.cancelDrop();
        } else {
            var oldParent = data.parent_internal_id;
            var nodeId = data.records[0].data.internal_id;

            // I came to CERN to create a new order!
            var newOrder;
            var newParent;
            var version = -2;
            console.log(dropPosition + " " + overModel.data.Name);
            if (dropPosition === 'append') {
                if (overModel.parentNode.data.root) {
                    // if it was appended to Path node
                    // in case path is not loaded yet
                    if (overModel.childNodes.length === 0) {
                        // magic number to show that desired action is to append node to the unloaded path
                        newOrder = -78;
                        version = this.getViewModel().get("idVer");
                    } else {
                        newOrder = overModel.childNodes.length + 1;
                    }
                } else {
                    newOrder = overModel.childNodes.length + 1;
                }
                newParent = overModel.data.internal_id;
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
            var view = this.getView();
            this.sendDnDrequest(nodeId, oldParent, newParent, newOrder, copy, version,
                function () {
                    // dropHandler.processDrop();
                    view.fireEvent("doSmthToAllNodes", data.view.panel.getRootNode().childNodes, newParent, oldParent, data.records[0], newOrder, data.records[0].data.Name, overModel.id, copy);
                });
            dropHandler.cancelDrop();
        }
    },

    doSmthToAllNodes: function (children, newParentId, oldParentId, orig, newOrder, name, newParentClientId, copy) {
        for (var i = 0, len = children.length; i < len; i++) {
            if (newOrder !== -78) {
                // adding
                if (children[i].data.internal_id === newParentId) {
                    children[i].insertChild(newOrder, this.copyDroppedRecord(orig));
                    // if not reordering in the same parent: in this case we handle updating orders only once, after removing is done.
                    if (newParentId !== oldParentId) {
                        this.update_orders(children[i].childNodes);
                    }

                }
            }
            // removing
            if (!copy) {
                if (children[i].data.internal_id === oldParentId) {
                    for (var k = 0, clen = children[i].childNodes.length; k < clen; k++) {
                        if (children[i].childNodes[k].data.Name === name) {
                            // if not reordering              or    reordering,                 but     not just added node
                            if ((newParentId !== oldParentId) || ((newParentId === oldParentId) && (children[i].childNodes[k].data.order <= k))) {
                                children[i].removeChild(children[i].childNodes[k]);
                                this.update_orders(children[i].childNodes);
                                break;
                            }
                        }
                    }
                }
            }
            this.doSmthToAllNodes(children[i].childNodes, newParentId, oldParentId, orig, newOrder, name, newParentClientId, copy);
        }
    },

    update_orders: function (children) {
        for (var i = 0, len = children.length; i < len; i++) {
            children[i].data.order = i;
            // console.log(children[i].data.Name + ' - ' + children[i].data.order);
        }
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

    sendDnDrequest: function (nodeId, oldParent, newParent, order, copied, version, _process_drop_callback) {
        // Can be replaced with just GET with params. It doesn't need to be more complicated than it can be
        var dndRequestObj = {
            'nodeId': nodeId,
            'oldParent': oldParent,
            'newParent': newParent,
            'order': order,
            'copied': copied
        };
        if (version > 0) {
            dndRequestObj['version'] = version;
        }
        Ext.Ajax.request({
            url: 'drag_n_drop',
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            jsonData: JSON.stringify(dndRequestObj),
            failure: function (response) {
                Ext.Msg.alert('Error', response.responseText);
                console.log(response);
            }, success: function (response) {
                // if (response.status == 200) {
                    _process_drop_callback();
                // }
            }
        });
    },

    addBeforeDragListener: function (tree) {
        var view = tree.getView(),
            dz = view.findPlugin('treeviewdragdrop');
        dz.dragZone.onBeforeDrag = function (data, e) {
            var rec = view.getRecord(e.getTarget(view.itemSelector));
            if (rec.parentNode.data.root) {
                return false;
            } else {
                data.parent_internal_id = rec.parentNode.data.internal_id;
            }
        };
        // dz.dropZone.onNodeDrop = function (nodeData, source, e, data) {
        //     //may be extended
        // };
    }

});
