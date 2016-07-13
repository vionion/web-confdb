
Ext.define("CmsConfigExplorer.view.module.Module",{
    extend: "Ext.panel.Panel",

    controller: "module-module",
    viewModel: {
        type: "module-module"
    },
    
    requires:['CmsConfigExplorer.view.module.ModuleGrid',
             'CmsConfigExplorer.view.module.ModuleParameters',
             'CmsConfigExplorer.view.module.ModuleController',
             'CmsConfigExplorer.view.module.ModuleModel'],
    
    alias: 'widget.moduletab',

    listeners:{
        loadModules: 'onLoadModules'
//        render: 'onLoadModules'
    },
    
    reference: 'moduleTab',
    viewConfig: {
        loadingHeight: 100
    },
    layout:{
        type: 'border'
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
            xtype: 'modulesgrid',
            height: '100%',
            viewConfig: {
                loadingHeight: 100
            },
    //        collapsible: true,
//            loadMask: true,
            listeners:{
                custGridModParams: 'onGridModParamsForward',
//                loadModules: 'onLoadModules',
                //afterrender: 'onModuleGridRender'
//                show: 'onModuleGridRender'
                render: 'onModuleGridRender'
                //scope: 'controller'
            }
        },
        {
        region: 'center',
        layout: 'fit',
        xtype: 'moduleparamstree',
        title: 'Parameters',
        split: true,
        height: '100%',
        width: '50%',
        loadMask: true
        
    }
    ]
});
