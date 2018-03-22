
Ext.define("CmsConfigExplorer.view.service.Service",{
    extend: "Ext.panel.Panel",
    
    alias: 'widget.servicetab',
    
    reference: 'servicetab',
    
    requires:['CmsConfigExplorer.view.service.ServicePrescaleTab',
             'CmsConfigExplorer.view.service.ServiceController',
             'CmsConfigExplorer.view.service.ServiceGrid',
             'CmsConfigExplorer.view.service.ServiceMessageLoggerTab',
             'CmsConfigExplorer.view.service.ServiceModel',
             'CmsConfigExplorer.view.service.ServiceParameters',
              'CmsConfigExplorer.view.service.PrescaleGrid'
             ],
    
    controller: "service-service",
    viewModel: {
        type: "service-service"
    },

    layout: {
        type: 'border'
    },
    
    items: [
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
            flex: 2,
            split: true,
            xtype: 'servicesgrid',
            height: '100%',
            loadMask: true,
            listeners:{
                rowclick: 'onServiceClick',
                custSrvParams: 'onGridSrvParamsForward',
                render: 'onRender',
                beforeshow: 'onRender'
        }

    },
    {
        region: 'center',
        xtype: 'tabpanel',
        flex: 4,
        reference: "centralPanel",
        header: false,
        split: true,
        height: '100%',
        layout: 'fit', 
        activeTab: 0,
        border: true,
        tabPosition: 'right',
        items: [
            {
                xtype: 'serviceparamstree',
                split: true,
                title: 'Service Params',
                reference: 'srvParamsTree',
                flex: 2,
                loadMask: true,
                listeners:{
//                    cusSrvparamsLoaded: 'onPrescaleTabRender'
                    load: 'onPrescaleTabRender'
                }
            }
        ]
    }
//    {
//        region: 'center',
//        xtype: 'panel',
//        flex: 3,
//        reference: "centralPanel",
//        header: false,
//        split: true,
//        height: '100%',
//        
//        layout:{
//            type: 'accordion',
//            titleCollapse: true,
//            animate: true
////            activeOnTop: true
//        },
//        
//        items:[
//            {
//                xtype: 'serviceparamstree',
//                split: true,
//                title: 'Service Params',
//                reference: 'srvParamsTree',
//                flex: 2,
//                loadMask: true,
//                listeners:{
////                    cusSrvparamsLoaded: 'onPrescaleTabRender'
//                    load: 'onPrescaleTabRender'
//                }
//            }
//        ]
//        
//    }    
    ]
});
