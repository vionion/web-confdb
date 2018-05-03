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
            if (dropPosition === 'append') {
                if (overModel.parentNode.data.root) {
                    // if it was appended to Path node
                    newOrder = overModel.lastChild.data.order + 1;
                } else {
                    newOrder = overModel.data.children[overModel.data.children.length - 1].order + 1;
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
            this.sendDnDrequest(nodeId, oldParent, newParent, newOrder, copy);
            dropHandler.processDrop();
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
