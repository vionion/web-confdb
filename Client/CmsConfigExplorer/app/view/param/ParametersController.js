Ext.define('InputTag', {
    extend: 'Ext.data.Model',

    fields: [
        {name: 'name', type: 'string'}
    ]

});

var inputTags = Ext.create('Ext.data.Store', {
    model: 'InputTag',
    autoLoad: false,
    proxy: {
        type: 'ajax',
        url: 'get_module_names',
        limitParam: '',
        pageParam: '',
        sortParam: '',
        startParam: '',
        noCache: false,
        headers: {'Content-Type': "application/json"},
        reader: {
            type: 'json',
            rootProperty: 'children'
        }
    }
 });

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
        console.log('inside tooltip activate');
        var idc = this.getViewModel().get("idCnf");
        var idv = this.getViewModel().get("idVer");
        var online = this.getViewModel().get("online");

        if(cid !=-1 && cid !=-2){
            //console.log("loading modules cnf");
            inputTags.load({params: {cnf: idc, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules");

        }
        else if (vid !=-1){
            //console.log("loading modules ver");
            inputTags.load({params: {ver: idv, online:online}});
//            this.lookupReference('modulesGrid').mask("Loading Modules");
        }
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
            // store: ['hltTest1', 'hltTest2', 'hltTest3']
            displayField : 'name'
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
        var parName = context.record.get('name');
        var type = context.record.get('paramtype');
        var valid = validate(context.value, type, function (valid_val) {
            context.value = valid_val;
            context.record.set('rendervalue', valid_val);
        });
        console.log(valid);
        if (valid) {
            var myObject = {'value': context.value, 'parName': parName, 'modId': modId};
            Ext.Ajax.request({
                url: 'update_param_val',
                // why the hell it doesn't work with UPDATE?
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                jsonData: JSON.stringify(myObject),
                failure: function (response) {
                    Ext.Msg.alert("Error");
                    console.log(response);
                }
            });
        }

    }



});

function validate(value, type, callback) {
    var valid = true;
    // string
    // console.log(bigInt(value));
    // var largeNumber = bigInt("9223372036854775807");
    // console.log(bigInt(value).leq(largeNumber));
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
        callback(value);
        valid = true;
    }
    //number
    else if (type === 'int32' || type === 'uint32' || type === 'int64' || type === 'uint64' || type === 'double') {
        if (isNaN(value)) {
            valid = false;
        } else {
            if ((type === 'uint32' || type === 'uint64') && value < 0) {
                valid = false;
            } else if ((type === 'uint32') || (type === 'int32')) {
                // between - 214748364 and 2147483647
                if ((value >> 0) != value) {
                    valid = false;
                }
            } else if (type === 'uint64' || type === 'int64') {
                // must be between -9223372036854775808 and 9223372036854775807
                // but check is between -9007199254740991 and 9007199254740991
                // (js range limitation)
                if (value > Number.MAX_SAFE_INTEGER || value < Number.MIN_SAFE_INTEGER) {
                    valid = false;

                }
            } else if (type === 'double') {
                // check must be added later
                valid = true;
            }
        }
    }
    // boolean, just one more time, why not
    else if (type === 'bool') {
        if (!((value === 'True') || (value === 'False'))) {
            valid = false;
        }
    }
    // InputTag: we don't really validate, but mark non-existing values with red
    else if (type === 'InputTag') {
        valid = true;
        if (inputTags.find('name', value) === -1) {
            alert('InputTag is not exists yet...');
        }
    } else {
        // all unusual types will revert changes, since something is wrong:
        console.log("Unchecked type: " + type + " value: " + value);
        valid = false;
    }

    return valid;
}