
Ext.define("Demo110315.view.esmodule.ESModule",{
    extend: "Ext.panel.Panel",

    controller: "esmodule-esmodule",
    viewModel: {
        type: "esmodule-esmodule"
    },
    
    requires:['Demo110315.model.ESModule',
             'Demo110315.model.ESModuleitem'],
    
    alias: 'widget.esmoduletab',
    
    listeners:{
        loadESModules: 'onLoadESModules'
    },
    
    reference: 'esModuleTab',
    
    layout:{
        type: 'border'
    },
    
    items:[
        {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
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
            xtype: 'esmodulesgrid',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                custGridESModParams: 'onGridESModParamsForward',
//                loadModules: 'onLoadESModules',
                render: 'onLoadESModules',
                afterrender: 'onESModuleGridRender'
                //scope: 'controller'
            }
        },
        {
        region: 'center',
        layout: 'fit',
        xtype: 'esmoduleparamstree',
        title: 'Parameters',
        split: true,
        height: '100%',
        width: '50%',
        loadMask: true
        
    }
    ]
});
