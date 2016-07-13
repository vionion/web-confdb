
Ext.define("CmsConfigExplorer.view.home.Home",{
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
            height: "25%",
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
                   margin: "30 0 0 0",
                    layout: {
                                type: 'hbox',
                                align: 'middle'
                                // pack: 'center'             
                            },
                    items:[
                        {
                            //logo
                            xtype: "image",
                            src: "resources/cms-logo.png",
                            width: 90, //"10%",
                            height: 90, //"80%",
                            margin: "0 20 0 85"

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
                            html: '<h1><font size="20" color="#000066" face="helvetica"> HLT Configurations web eXplorer</font></h1>'
                        },
                        {
                            xtype: 'tbtext',
                            height : '30%',
                            bind:{
                                text: '{appversion}'
                            },
                            style: {
                                color: '#000066'
                            }
                        }         
                    ] 
                },
                {
                    xtype: 'panel',
                    header: false,
                    border: false,
                    width: "90%",
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
                        margin: "40 0 0 0",
                        listeners: {
                                click: 'onExploreDatabaseClick',
                                scope: 'controller'
                        }
//                        iconCls: ".main-button-icon"
                    }
//                     ,{
//                         xtype: "button",
//                         textAlign: "center",
//                         disabled: true,
// //                        icon: "resources/db_button.jpeg",
//                         text: "<h3>Import Configuration</h3>",
//                         width: 260, //"50%",
//                         height: 60, //"40%",
//                         scale   : 'large',
//                         margin: "50 0 0 0"
// //                        iconCls: ".main-button-icon"
//                     }
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
                        margin: "40 0 0 0",
                        listeners: {
                                click: 'onImportPythonClick',
                                scope: 'controller'
                        }
//                        iconCls: ".main-button-icon"
                    }
//                     ,{
//                         xtype: "button",
// //                        icon: "resources/db_button.jpeg",
//                         textAlign: "center",
//                         disabled: true,
//                         text: "<h3>Run Custom Script</h3>",
//                         width: 260, //"50%",
//                         height: 60, //"40%",
//                         scale   : 'large',
//                         margin: "50 0 0 0"
// //                        iconCls: ".main-button-icon"
//                     }
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
                        text: "<h3>Run Custom Script</h3>",
                        width: 260, //"50%",
                        height: 60, //"40%",
                        scale   : 'large',
                        margin: "40 0 0 0"
//                        iconCls: ".main-button-icon"
                    }
//                     ,{
//                         xtype: "button",
// //                        icon: "resources/db_button.jpeg",
//                         textAlign: "center",
//                         disabled: true,
// //                        text: "<h3>Feature T D</h3>",
//                         width: 260, //"50%",
//                         height: 60, //"40%",
//                         scale   : 'large',
//                         margin: "50 0 0 0"
// //                        iconCls: ".main-button-icon"
//                     }
                ]
            }
        ]
    }
    ,{
            region: 'south',
            xtype: 'panel',
            header: false,        
            height: '52%',
            width: '100%',
            layout: {
                type: 'vbox',
                align: 'middle',
                pack: 'start'
            },
            items: [
                {
                    xtype: 'textfield',
                    margin: "5 0 0 0",
                    labelWidth: 280,
                    height: 100,
                    width: '55%',
                    labelSeparator: "",
                    labelAlign: "top",
                    labelClsExtra: 'label-center-align-class',
                    fieldLabel: '<p><font size="9" color="#2e2eb8" face="helvetica"> Open Menu </font></p>', //# 194de6
                    reference: 'openmenufield',
                    emptyText: "Type the Menu name/path - Version is not mandatory",

            //                triggerWrapCls: 'x-form-clear-trigger',
                    listeners: {
                        specialkey: 'onEnterKey',
                        scope: 'controller'
                        
                    }

                }
            ]
            
        }
    ]
});
