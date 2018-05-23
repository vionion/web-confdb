
Ext.define("CmsConfigExplorer.view.streamdataset.EventContent",{
    extend: "Ext.grid.Panel",
    
    requires:['CmsConfigExplorer.view.streamdataset.EventContentController'],
    
    controller: "streamdataset-eventcontent",
    
    alias: 'widget.eventcontent',
    
    reference: "eventContentGrid",
    
    bind:{
        store:'{ecstats}'
    },

    scrollable: true,

    plugins: {
        ptype: 'cellediting',
        clicksToEdit: 2,
        listeners: {
            edit: 'onEditDone'
        }
    },

    dockedItems: [{
        xtype: 'toolbar',
        dock: 'top',
        
                    items:[ 
                    {
                        text: 'Keep',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop',
                        disabled: true
//                        listeners: {
//                            click: 'onDropClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Keep All',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepAllClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop All',
                        disabled: true
//                        listeners: {
//                            click: 'onDropAllClick',
//                            scope: 'controller'
//                        }
                    }
            ] 
    
    }],

    columns: [
        {
            xtype: 'gridcolumn',
            header: 'Type',
            dataIndex: 'stype',
            flex: 1,
            editor: {
                xtype: 'combobox',
                store: ['drop', 'keep'],
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
            }
        },
        {
            xtype: 'gridcolumn',
            header: 'Class Name',
            dataIndex: 'classn',
            flex: 1,
            editor: {
                xtype: 'textfield',
                editable: true
            }
        },
        {
            xtype: 'gridcolumn',
            header: 'Module element',
            dataIndex: 'modulel',
            flex: 1,
            editor: {
                xtype: 'combo',
                queryMode: 'local',
                autoLoad: false,
                // to allow freetype
                forceSelection: false,
                hideTrigger: true,
                typeAhead: true,
                store: inputTags,
                displayField: 'name'
            },
            renderer: function (v, meta) {
                if (v && (inputTags.findExact('name', v.split(":")[0]) === -1)  && v !== '*') {
                    meta.style = "color:red;";
                }
                return v;
            }
        },
        {
            xtype: 'gridcolumn',
            header: 'Extra name',
            dataIndex: 'extran',
            flex: 1,
            editor: {
                xtype: 'textfield',
                editable: true
            }
        },
        {
            xtype: 'gridcolumn',
            header: 'Process name',
            dataIndex: 'processn',
            flex: 1,
            editor: {
                xtype: 'textfield',
                editable: true
            }
        }
    ]
    
});
