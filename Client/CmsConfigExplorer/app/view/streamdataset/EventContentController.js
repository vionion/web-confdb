Ext.define('CmsConfigExplorer.view.streamdataset.EventContentController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.streamdataset-eventcontent',

    send_add_line_request: function (drop_line) {
        var internal_id = this.getViewModel().getStore('ecstats').first().get('internal_id');
        var statement_request = {
            'internal_id': internal_id,
            'drop_line': drop_line
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

    onKeepClick: function () {
        this.send_add_line_request(false);
    },

    onDropClick: function () {
        this.send_add_line_request(true);
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
                        'statementrank': statementrank
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
        var regex_start = new RegExp("^\"");

        while (regex_start.test(value)) {
            value = value.replace(/^"/g, "");
        }

        var regex_end = new RegExp("\"$");
        while (regex_end.test(value)) {
            value = value.replace(/"$/g, "");
        }

        var regex_inner_quote = new RegExp("([^\\\\])(\")");
        while (regex_inner_quote.test(value)) {
            value = value.replace(regex_inner_quote, "$1\\$2");
        }

        // value = '"' + value;
        // value = value + '"';
        callback(valid, value);
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
    // InputTag: we don't really validate, but mark non-existing values with red
    else if (type === 'modulel') {
        valid = true;
        if (!value || value === '""' || value === "''") {
            valid = false;
            callback(valid, prevVal);
        } else if ((inputTags.findExact('name', value.split(":")[0]) === -1)  && value !== '*') {
            Ext.MessageBox.confirm('Confirm', 'This module doesn\'t exists yet. Do you really want to change this InputTag value?', function (btn) {
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
