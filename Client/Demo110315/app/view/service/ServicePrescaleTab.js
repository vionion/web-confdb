
Ext.define("Demo110315.view.service.ServicePrescaleTab",{
    extend: "Ext.panel.Panel",

    alias: 'widget.prescaletab',
    
    reference: 'prescaleTab',
    
    controller: "service-serviceprescaletab",
    
    layout: {
        type: 'vbox',
        align: 'stretch'
    },
    title: 'Prescale Table',
    items: [
        {
            xtype: 'toolbar',
//            region: 'north',
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
        }
//        ,{
//            xtype: 'grid',
//            region: 'center',
//            reference: 'prescaleGrid',
//            columns: [
//                    {
//                        xtype: 'gridcolumn',
//                        text: 'Path Name',
//                        flex: 1,
//                        dataIndex: 'name'
//                    }
//                ]
//        }
    ]
});
