
Ext.define("Demo110315.view.service.Service",{
    extend: "Ext.panel.Panel",
    
    alias: 'widget.servicetab',
    
    reference: 'servicetab',
    
    requires:['Demo110315.view.service.ServicePrescaleTab'],
    
    controller: "service-service",
    viewModel: {
        type: "service-service"
    },

    layout: {
        type: 'border'
    },
    
    items: [
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
        flex: 3,
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
