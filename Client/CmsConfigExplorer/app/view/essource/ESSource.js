
Ext.define("CmsConfigExplorer.view.essource.ESSource",{
    extend: "Ext.panel.Panel",
    
    requires:['CmsConfigExplorer.view.essource.ESSourceParameters',
             'CmsConfigExplorer.view.essource.ESSourceModel',
             'CmsConfigExplorer.view.essource.ESSourceController',
             'CmsConfigExplorer.view.essource.ESSourceGrid'],
    
    controller: "essource-essource",
    viewModel: {
        type: "essource-essource"
    },

    alias: 'widget.essourcetab',
    
    listeners:{
        loadESModules: 'onLoadESSource'
    },
    
    reference: 'esSourceTab',
    
    layout:{
        type: 'border'
    },
    viewConfig: {
        loadingHeight: 100
    },
    
    items:[
//        {
//            xtype: 'toolbar',
//            region: 'north',
//            paddingLeft: 5,
//            items:[ 
//                    {
//                        xtype: 'textfield',
//                        fieldLabel: 'Search',
//                        labelWidth: 47,
//                        enableKeyEvents: true,
//                        disabled: true
//                    }
//                ]
//        },
        {
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'essourcegrid',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                custGridESSourceParams: 'onGridESSourceParamsForward',
                render: 'onLoadESSource',
//                loadModules: 'onLoadEDSource',
                afterrender: 'onESSourceGridRender'
                //scope: 'controller'
            }
        },
        {
        region: 'center',
        layout: 'fit',
        xtype: 'essourceparamstree',
        title: 'Parameters',
        split: true,
        height: '100%',
        width: '50%',
        loadMask: true,
        viewConfig: {
            loadingHeight: 100
        }
        
    }
    ]
});
