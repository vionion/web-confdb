
Ext.define("Demo110315.view.streamdataset.EventContentPanel",{
    extend: "Ext.panel.Panel",

    requires:['Demo110315.view.streamdataset.EventContent'],
    
    controller: "streamdataset-eventcontentpanel",
    
    alias: 'widget.evcopanel',
    
    reference: 'evcoPanel',
    layout:{
        type:'border'
    },
    items:[
        {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
                    {
                        text: 'Keep',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop',
                        disabled: true
//                        listeners: {
//                            click: 'onDropClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Keep All',
                        disabled: true
//                        listeners: {
//                            click: 'onKeepAllClick',
//                            scope: 'controller'
//                        }
                    },
                    {
                        text: 'Drop All',
                        disabled: true
//                        listeners: {
//                            click: 'onDropAllClick',
//                            scope: 'controller'
//                        }
                    }
            ]  
        },
        {
            xtype: 'eventcontent',
            region: 'center',
            loadMask: true
        }
    ]
});
