
Ext.define("Demo110315.view.home.Home",{
    extend: "Ext.container.Container",
    
    alias: "widget.home",
    
    controller: "home-home",
    viewModel: {
        type: "home-home"
    },

    layout: {
        type: 'border'
    },

    reference: "home",
//    height: '100%',
    
    items: [
        {
            xtype: 'panel',
            header: false,
            border: false,
            region: "north",
            height: "30%",
//            width: "100%",
            layout:{
                type: 'vbox',
                align: 'middle'
            },
            items:[
                {
                    xtype: "panel",
                    flex: 1,
                    width: "100%",
        //            border: "0 0 1 0",

        //            stretch: true,
        //            margin: "0 0 0 0",
                    layout: {
                                type: 'hbox',
                                align: 'middle'
//                                pack: 'center'             
                            },
                    items:[
                        {
                            //logo
                            xtype: "image",
                            src: "resources/cms-logo.png",
                            width: 120, //"10%",
                            height: 120, //"80%",
                            margin: "0 0 0 50"

        //                    flex: 1,
        //                    padding: "0,20,0,20",
                        },{
                            xtype: "panel",
                            header: false,
                            margin: "25 0 0 25",
                            align: 'middle',
        //                    height: "100%",
        //                    align: 'middle',
        //                    padding: "0 0 0 50",
        //                    flex: 1,
                            html: '<h1><font size="20" color="black" face="verdana"> CMS - HLT Configurations </font></h1>'
                        }
                    ] 
                },
                {
                    xtype: 'panel',
                    header: false,
                    border: false,
                    width: "93%",
                    html: "<hr>"
                }
            ]
        },
        {
        region: 'center',
        xtype: 'panel',
        header: false,
//        frame: true,
//        border: false,
        layout: {
            type: 'hbox'
        },
        items: [
            {
                xtype: 'panel',
                header: false,
//                html: '<h1><font size="10" color="black" face="verdana"> CMS HLT </font></h1>',
//                flex: 1,
                frame: false,
                height: "100%",
                width: "33%",
                bodyStyle: {
                    border: '1 0 0 0'
                    
                },
                bodyBorder: true,
                layout: {
                            type: 'vbox',
//                            pack: 'center',
                            align: 'end'
                        },
                items:[
                    {
                        xtype: "button",
//                        icon: "resources/db_button.jpeg",
                        text: "<h3>Explore Database</h3>",
                        textAlign: "center",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0",
                        listeners: {
                                click: 'onExploreBatabaseClick',
                                scope: 'controller'
                        }
//                        iconCls: ".main-button-icon"
                    },
                    {
                        xtype: "button",
                        textAlign: "center",
                        disabled: true,
//                        icon: "resources/db_button.jpeg",
                        text: "<h3>Import Configuration</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0"
//                        iconCls: ".main-button-icon"
                    }
                ]
            },
            {
                xtype: 'panel',
                header: false,
//                html: '<h1><font size="10" color="black" face="verdana"> CMS HLT </font></h1>', 
                flex: 1,
                frame: false,
                hidden: false,
                width: "33%",
                height: "100%",
                layout: {
                            type: 'vbox',
//                            pack: 'center',
                            align: 'middle'
                        },
                items:[
                    {
                        xtype: "button",
//                        icon: "resources/db_button.jpeg",
                        textAlign: "center",
                        disabled: true,
                        text: "<h3>Import Python file</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0"
//                        iconCls: ".main-button-icon"
                    },
                    {
                        xtype: "button",
//                        icon: "resources/db_button.jpeg",
                        textAlign: "center",
                        disabled: true,
                        text: "<h3>Run Custom Script</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0"
//                        iconCls: ".main-button-icon"
                    }
                ]
            },
            {
                xtype: 'panel',
                header: false,
//                html: '<h1><font size="10" color="black" face="verdana"> CMS HLT </font></h1>',
                flex: 1,
                frame: false,
                hidden: false,
                width: "33%",
                height: "100%",
                layout: {
                            type: 'vbox',
//                            pack: 'center',
                            align: 'begin'
                        },
                items:[
                    {
                        xtype: "button",
//                        icon: "resources/db_button.jpeg",
                        textAlign: "center",
                        disabled: true,
//                        text: "<h3>Feature T D</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0"
//                        iconCls: ".main-button-icon"
                    },
                    {
                        xtype: "button",
//                        icon: "resources/db_button.jpeg",
                        textAlign: "center",
                        disabled: true,
//                        text: "<h3>Feature T D</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "50 0 0 0"
//                        iconCls: ".main-button-icon"
                    }
                ]
            }
        ]
    }]
});
