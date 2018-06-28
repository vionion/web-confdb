Ext.define('CmsConfigExplorer.view.param.ParametersController', {
    extend: 'Ext.app.ViewController',
    alias: 'controller.parameters',

    onTooltipActivate: function (grid) {

        var view = grid.getView();
        var tip = Ext.create('Ext.tip.ToolTip', {
            // The overall target element.
            target: view.el,
            // Each grid row causes its own separate show and hide.
            delegate: view.itemSelector,
            // Moving within the row should not hide the tip.
            trackMouse: true,
            // Render immediately so that tip.body can be referenced prior to the first show.

            listeners: {
                // Change content dynamically depending on which element triggered the show.
                beforeshow: function updateTipBody(tip) {
                    tip.update(view.getRecord(tip.triggerElement).get('rendervalue'));
                }
            }

        });
    }

    , onBeforeCellEdit: function (editor, context, eOpts) {

        var col = context.column;
        var value = context.value;
        var editor_area = new Ext.grid.plugin.CellEditing({
            xtype: 'textarea',
            editable: true,
            grow: true,
            growMin: 0
        });

        var editor_field = new Ext.grid.plugin.CellEditing({
            xtype: 'textfield',
            editable: true
        });

        var editor_bool = new Ext.grid.plugin.CellEditing({
            xtype: 'combobox',
            store: ['False', 'True'],
            allowBlank: false,
            forceSelection: true,
            editable: true,
            onFocus: function () {
                var bool = this;
                if (!bool.isExpanded) {
                    bool.expand()
                }
                bool.getPicker().focus();
            }
        });

        var editor_tags = new Ext.grid.plugin.CellEditing({
            xtype: 'combo',
            queryMode: 'local',
            autoLoad: false,
            // to allow freetype
            forceSelection: false,
            hideTrigger: true,
            typeAhead: true,
            store: inputTags,
            displayField: 'name'
        });
        if (col.getEditor().editable) {
            if (context.record.get('paramtype') === 'bool') {
                col.setEditor(editor_bool);
            } else if (context.record.get('paramtype') === 'InputTag') {
                col.setEditor(editor_tags);
            } else if (value.length > 70) {
                col.setEditor(editor_area);
            } else {
                col.setEditor(editor_field);
            }

        }
        return true;
    },

    onEditDone: function (editor, context, eOpts) {

        var modId = context.record.get('moduleId');
        // hmm, maybe it is time to change it to internal_id?
        var parName = context.record.get('name');
        var type = context.record.get('paramtype');
        var prevVal = context.value;
        if (context.record.modified !== null) {
            prevVal = context.record.modified.rendervalue;
        }
        var vid = this.getViewModel().get("idVer");
        validate(context.value, prevVal, type, function (valid, validValue) {
                context.value = validValue;
                context.record.modified = {rendervalue: validValue};
                context.record.set('rendervalue', validValue);
                if (valid) {
                    var myObject = {'value': context.value, 'parName': parName, 'modId': modId, ver_id: vid};
                    Ext.Ajax.request({
                        url: 'update_param_val',
                        // why the hell it doesn't work with UPDATE?
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        jsonData: JSON.stringify(myObject),
                        failure: function (response) {
                            Ext.Msg.alert("Error");
                            console.log(response);
                        },
                        success: function () {
                            context.record.set('isDefault', "False");
                        }
                    });
                }
            }
        );

    }


});

var MAX_INTEGER = bigInt("9223372036854775807");
var MAX_UNSIGNED_INTEGER = bigInt("18446744073709551615");
var MIN_INTEGER = bigInt("-9223372036854775808");

function validate(value, prevVal, type, callback) {
    var valid = true;
    // string
    if (type === 'string') {
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

        value = '"' + value;
        value = value + '"';
        callback(valid, value);
    }
    //number
    else if (type === 'int32' || type === 'uint32' || type === 'int64' || type === 'uint64' || type === 'double') {
        if (isNaN(value)) {
            valid = false;
        } else {
            if (type === 'uint32' || type === 'uint64') {
                if (value < 0) {
                    valid = false;
                } else if (type === 'uint32') {
                    // between 0 and 4294967295
                    if ((value >>> 0) != value) {
                        valid = false;
                    }
                } else if (type === 'uint64') {
                    var bigVal = bigInt(value);
                    if (bigVal.greater(MAX_UNSIGNED_INTEGER)) {
                        valid = false;
                    }
                }
            } else if (type === 'int32') {
                // between -2147483648 and 2147483647
                if ((value >> 0) != value) {
                    valid = false;
                }
            } else if (type === 'int64') {
                // between -9223372036854775808 and 9223372036854775807
                var bigVal = bigInt(value);
                if (bigVal.greater(MAX_INTEGER) || bigVal.lesser(MIN_INTEGER)) {
                    valid = false;
                }
            } else if (type === 'double') {
                valid = true;
            }
        }
        if (valid) {
            callback(valid, value);
        } else {
            callback(valid, prevVal);
        }
    }
    // boolean, just one more time, why not
    else if (type === 'bool') {
        if (!((value === 'True') || (value === 'False'))) {
            valid = false;
            callback(valid, prevVal);
        } else {
            callback(valid, value);
        }
    }
    // InputTag: we don't really validate, but mark non-existing values with red
    else if (type === 'InputTag') {
        valid = true;
        if (!value || value === '""' || value === "''") {
            valid = false;
            callback(valid, prevVal);
        } else if (inputTags.findExact('name', value.split(":")[0]) === -1) {
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