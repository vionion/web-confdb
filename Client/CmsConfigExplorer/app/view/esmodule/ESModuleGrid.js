
Ext.define('CmsConfigExplorer.view.esmodule.ESModuleGrid',{
    extend: "Ext.tree.Panel",
    
    requires:['CmsConfigExplorer.view.esmodule.ESModuleGridController'],
    
    controller: "esmodule-esmodulegrid",

    alias: 'widget.esmodulesgrid',

    listeners: {
        rowclick: 'onGridESModuleClick',
        scope: 'controller'    
    },
    
    bind:{
        // bind store to view model "modules" store
        store:'{esmodules}',
        selection: '{selectedESModule}'
 
    },
    
    listeners: {
        rowclick: 'onGridESModuleClick',
        scope: 'controller'    
    },
    viewConfig: {
        loadingHeight: 100
    },
    loadMask: true,
    
    reference: 'esModulesGrid',

    header: false,
    
    dockedItems: [{
        xtype: 'toolbar',
        reference: 'esmodHeaderTooolBar',
        dock: 'top',

        items: [
            { 
                xtype: 'tbtext',
                text: '<b>ES Modules</b>'
            },
            {
                xtype: 'tbseparator'
            },
            {
                labelWidth: 150,
                xtype: 'textfield',
                fieldLabel: 'ES Module search',
                reference: 'esmodtrigfield',
//                triggerWrapCls: 'x-form-clear-trigger',
                triggers:{
                    search: {
                        reference: 'esmodTriggerSearch',
                        cls: 'x-form-clear-trigger',
                        handler: 'onEsModTriggerClick',
                        listeners: {
                            change: 'onESModuleSearchChange'

                        }
                    }
                }, 
                listeners: {
                    change: 'onESModuleSearchChange'
                    
                }
            }
            ,{
                xtype: 'displayfield',
                reference: 'esmodMatches',
                fieldLabel: 'Matches',

                // Use shrinkwrap width for the label
                labelWidth: null

            }
        ]
    }],
    
    useArrows: true,
    columns: [
        {
            xtype: 'treecolumn',
            text: 'Name',
            flex: 2,
            dataIndex: 'name'
        },
        {
            xtype: 'gridcolumn',
            text: 'Class',
            flex: 1,
            dataIndex: 'mclass'

        }
    ]
});
