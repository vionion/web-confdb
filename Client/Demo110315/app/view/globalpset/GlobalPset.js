Ext.define("Demo110315.view.globalpset.GlobalPset", {
        extend: "Ext.panel.Panel",

        alias: 'widget.globalpsettab',

        reference: 'globalpsettab',
        
        requires:['Demo110315.view.globalpset.GlobalPsetParamsTree',
                 'Demo110315.view.globalpset.GlobalPsetTree'],
    
        controller: "globalpset-globalpset",
        viewModel: {
            type: "globalpset-globalpset"
        },

        layout: {
            type: 'border'
        },

        items: [
            {
                xtype: 'toolbar',
                region: 'north',
                paddingLeft: 5,
                items: [
                    {
                        xtype: 'textfield',
                        fieldLabel: 'Search',
                        labelWidth: 47,
                        enableKeyEvents: true,
                        disabled: true
                    }
                ]
        },
            {
                region: 'west',
                flex: 1,
                split: true,
                xtype: 'gpsettree',
                height: '100%',
                loadMask: true,
                listeners: {
                    rowclick: 'onGpsetClick',
                    custSrvParams: 'onTreeGpsetParamsForward',
                    render: 'onRender',
                    beforeshow: 'onRender'
                }

    },
            {
                region: 'center',
                xtype: 'panel',
                flex: 3,
                reference: "centralGpsetPanel",
                header: false,
                split: true,
                height: '100%',

                layout: {
                    type: 'fit'
                },

                items: [
                    {
                        xtype: 'gpsetparamstree',
                        split: true,
                        title: 'Global Pset Parameters',
                        reference: 'gpsetParamsTree',
                        flex: 2,
                        loadMask: true,
                        listeners: {
                        }
            }

        ]

    }
    ]
});
