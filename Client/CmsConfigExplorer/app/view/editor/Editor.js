
Ext.define("CmsConfigExplorer.view.editor.Editor",{
    extend: "Ext.panel.Panel",
    
    alias: 'widget.confeditor',
    
    reference: 'confeditor',
    
    requires:['CmsConfigExplorer.view.details.*',
                'CmsConfigExplorer.view.editor.EditorController',
                'CmsConfigExplorer.view.editor.EditorModel',
                'CmsConfigExplorer.view.summary.*',
                'Ext.Ajax',
                'Ext.plugin.AbstractClipboard'
             ],
    
    controller: "editor-editor",
    viewModel: {
        type: "editor-editor"
    },
    
    layout: {
//        type: 'vbox',
//        align: 'stretch'
        type: 'border'
    },
    
    listeners:{
        beforerender: 'onBeforeRender'
    },

     items: [
            {
                region: 'north',
                xtype: 'toolbar',
                reference: 'editTool',
                paddingLeft: 5,
                items:[
                        {
                            xtype: "image",
                            src: "resources/cms-logo.png",
                            width: 30, //"10%",
                            height: 30 //"80%",
//                            margin: "0 0 0 50"
                        },{
                            xtype: 'tbtext',
                            bind: {
                                 text: '<b>HLT Configuration Editor - {appversion}</b>' 
                            }
                            
                        },
                        {
                            text: 'Home',
                            listeners: {
                                click: 'onHomeClick',
                                scope: 'controller'
                            }
                        },
                        {
                            text: 'Explore',
                            listeners: {
                                click: 'onExploreClick',
                                scope: 'controller'
                            }
                        },
                        {
                            text: 'Details View',
                            reference: 'detailsbutton',
                            listeners: {
                                click: 'onDetailsClick',
                                scope: 'controller'
                            }
                        },
                        {
                            text: 'Summary View',
                            disabled: true,
                            reference: 'summarybutton',
                            listeners: {
                                click: 'onSummaryClick',
                                scope: 'controller'
                            }
                        },
                        {
                            text: 'Save',
                            disabled: true
                        },
                        {
                            text: 'Import',
                            disabled: true
                        },
                        {
                            text: 'Export',
//                            disabled: true,
                            reference: 'exportbutton',
                            listeners: {
                                click: 'onExportClick',
                                scope: 'controller'
                            }
                        },
                        {
                            xtype: 'tbtext',
                            text: '<b>Loading... </b>',
                            hidden: true,
                            reference: 'loadingtext'
                        },
                        {
                            xtype: "image",
                            src: "resources/loading.gif",
                            width: 20, //"10%",
                            height: 20, //"80%",
//                            margin: "0 0 0 50"
                            hidden: true,
                            reference: 'loadinggif'
                        },
                        '-',
                        {
                            xtype: 'tbtext',
                            text: '<b>Configuration:</b>'   
                        },
                        {
                            xtype: 'tbtext',
                            bind:{
                                text: '{cnfname}'
                            }
                        },
                        '-'
//                        {
//                            xtype: 'tbtext',
//                            text: '<b>Link: </b>'   
//                        },
//                        ,{
////                            xtype: 'button',//'tbtext',
//                            text: 'External link',
//                            tooltip: 'This is a link to this configuration',
//
////                            bind:{
////                                text: '{link}'
////                            },
//                            listeners: {
//                                click: 'onLinkClick',
//                                scope: 'controller'
//                            }
//                        }                   
                    ] 
            },
            {
                region: 'center',
                xtype: 'panel',
                layout: 'card',
                reference: 'cardspanel',
                items: [
                    {
//                        id: 'card-summary',
                        xtype: 'summaryview',
                        reference: 'summaryview'
                    }
                    ,{
//                        id: 'card-details',
                        xtype: 'detailsview',
                        reference: 'detailsview'
                    }
                ]

            }
    ]
});
