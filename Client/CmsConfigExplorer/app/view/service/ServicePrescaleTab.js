
Ext.define("CmsConfigExplorer.view.service.ServicePrescaleTab",{
    extend: "Ext.panel.Panel",
    
    requires:['CmsConfigExplorer.view.service.PrescaleGrid',
             'CmsConfigExplorer.view.service.ServicePrescaleTabController'],
    
    alias: 'widget.prescaletab',
    
    reference: 'prescaleTab',
    
    controller: "service-serviceprescaletab",
    
    layout: {
//        type: 'vbox',
//        align: 'stretch'
        type: 'border'
    },
    title: 'Prescale Table',
//    enableLocking: true,
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
//        }

    ]
});

