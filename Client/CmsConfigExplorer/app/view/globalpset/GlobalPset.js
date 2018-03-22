Ext.define('CmsConfigExplorer.view.globalpset.GlobalPset', {
        extend: "Ext.panel.Panel",

        alias: 'widget.globalpsettab',

        reference: 'globalpsettab',
        
        requires:['CmsConfigExplorer.view.globalpset.GlobalPsetParamsTree',
                 'CmsConfigExplorer.view.globalpset.GlobalPsetTree',
                 'CmsConfigExplorer.view.globalpset.GlobalPsetController',
                 'CmsConfigExplorer.view.globalpset.GlobalPsetModel'],
    
        controller: "globalpset-globalpset",
        viewModel: {
            type: "globalpset-globalpset"
        },

        layout: {
            type: 'border'
        },

        items: [
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
                    beforeshow: 'onRender',
                    cusAlphaOrderClickForward: 'onSortAlphaPaths',
                    cusOrigOrderClickForward: 'onSortOriginalPaths'
                }

    },
            {
                region: 'center',
                xtype: 'panel',
                flex: 1,
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
