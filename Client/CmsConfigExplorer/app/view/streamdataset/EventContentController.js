Ext.define('CmsConfigExplorer.view.streamdataset.EventContentController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-eventcontent',

    send_add_line_request: function (drop_line) {
        var streamsTab = this.getView().up().up();
        var internal_id = streamsTab.lookupReference('streamTree').getSelectionModel().getSelection()[0].data.internal_id;
        var ver_id = this.getViewModel().get("idVer");
        var statement_request = {
            'internal_id': internal_id,
            'drop_line': drop_line,
            'ver_id': ver_id
        };
        var store = this.getViewModel().getStore('ecstats');
        Ext.Ajax.request({
            url: 'add_event_statement',
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            jsonData: JSON.stringify(statement_request),
            failure: function (response) {
                Ext.Msg.alert('Error', response.responseText);
                console.log(response);
            }, success: function (response) {
                store.add(Ext.decode(response.responseText));
            }
        });
    },

    send_delete_line_request: function () {
        var grid = this.getView();
        var selectedRecord = grid.getSelectionModel().getSelection()[0];
        if (selectedRecord) {
            var streamsTab = this.getView().up().up();
            var internal_id = streamsTab.lookupReference('streamTree').getSelectionModel().getSelection()[0].data.internal_id;
            var statementrank = selectedRecord.data.statementrank;
            if (statementrank > 0) {
                var statement_request = {
                    'internal_id': internal_id,
                    'rank': statementrank
                };
                var store = this.getViewModel().getStore('ecstats');
                Ext.Ajax.request({
                    url: 'delete_event_statement',
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    jsonData: JSON.stringify(statement_request),
                    failure: function (response) {
                        Ext.Msg.alert('Error', response.responseText);
                        console.log(response);
                    }, success: function (response) {
                        store.remove(selectedRecord);
                        store.reload();
                    }
                });
            }
        }
    },

    onKeepClick: function () {
        this.send_add_line_request(false);
    },

    onDropClick: function () {
        this.send_add_line_request(true);
    },

    onDeleteLine: function () {
        this.send_delete_line_request();
    },

    onEditDone: function (editor, context, eOpts) {

        var column = context.column.config.dataIndex;
        var internal_id = context.record.get('internal_id');
        var statementrank = context.record.get('statementrank');
        var prevVal = context.value;
        if (context.record.modified) {
            prevVal = context.record.modified[column];
        } else {
            context.record.modified = {};
        }
        var ver_id = this.getViewModel().get("idVer");
        validateEvent(context.value, prevVal, column, function (valid, validValue) {
                context.value = validValue;
                context.record.modified[column] = validValue;
                context.record.set(column, validValue);
                if (valid) {
                    if (column === 'stype') {
                        column = 'statementtype';
                        context.value = context.value === 'keep' ? 1 : 0;
                    }
                    var statement_request = {
                        'value': context.value,
                        'column': column,
                        'internal_id': internal_id,
                        'statementrank': statementrank,
                        'ver_id': ver_id
                    };
                    Ext.Ajax.request({
                        url: 'update_event_statement',
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        jsonData: JSON.stringify(statement_request),
                        failure: function (response) {
                            Ext.Msg.alert("Error");
                            console.log(response);
                        }
                    });
                }
            }
        );

    }


});


function validateEvent(value, prevVal, type, callback) {
    var valid = true;
    // string
    if (type === 'classn' || type === 'extran' || type === 'processn') {
        var regex_spaces = new RegExp(" ");
        var regex_quotes = new RegExp("[\"\']");

        if (regex_quotes.test(value) || regex_spaces.test(value)) {
            valid = false;
            callback(valid, prevVal);
        } else if (type !== 'extran' && !value){
            valid = false;
            callback(valid, prevVal);
        } else {
            callback(valid, value);
        }
    }

    // stype, just one more time, why not
    else if (type === 'stype') {
        if (!((value === 'keep') || (value === 'drop'))) {
            valid = false;
            callback(valid, prevVal);
        } else {
            callback(valid, value);
        }
    }
    // module element: we don't really validate, but mark non-existing values with red
    else if (type === 'modulel') {
        valid = true;
        if (!value || value === '""' || value === "''") {
            valid = false;
            callback(valid, prevVal);
        } else if ((inputTags.findExact('name', value.split(":")[0]) === -1)  && value !== '*') {
            Ext.MessageBox.confirm('Confirm', 'This module doesn\'t exists yet. Do you really want to change this value?', function (btn) {
                if (btn === 'no') {
                    callback(valid, prevVal);
                } else {
                    callback(valid, value);
                }
            });
        } else {
            callback(valid, value);
        }
    } else {
        // all unusual types will revert changes, since something is wrong:
        console.log("Unchecked type: " + type + " value: " + value);
        valid = false;
        callback(valid, prevVal);
    }

}
