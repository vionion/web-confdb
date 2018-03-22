
Ext.define('CmsConfigExplorer.view.esmodule.ESModule',{
    extend: "Ext.panel.Panel",
    
    requires:['CmsConfigExplorer.view.esmodule.ESModuleParameters',
             'CmsConfigExplorer.view.esmodule.ESModuleModel',
             'CmsConfigExplorer.view.esmodule.ESModuleController',
             'CmsConfigExplorer.view.esmodule.ESModuleGrid'],
    
    controller: "esmodule-esmodule",
    viewModel: {
        type: "esmodule-esmodule"
    },
    
    requires:['CmsConfigExplorer.model.ESModule',
             'CmsConfigExplorer.model.ESModuleitem'],
    
    alias: 'widget.esmoduletab',
    
    listeners:{
        loadESModules: 'onLoadESModules'
    },
    
    reference: 'esModuleTab',
    
    layout:{
        type: 'border'
    },
    viewConfig: {
        loadingHeight: 100
    },
    
    items:[
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
