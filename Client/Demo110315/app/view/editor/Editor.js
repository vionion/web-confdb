
Ext.define("Demo110315.view.editor.Editor",{
    extend: "Ext.panel.Panel",
    
    alias: 'widget.confeditor',
    
    requires:['Demo110315.model.Moduleitem',
             'Demo110315.model.Pathitem',
             'Demo110315.view.path.Path',
             'Demo110315.view.path.Parameters',
             'Demo110315.view.path.Pathtree',
             'Demo110315.view.module.Module',
             'Demo110315.model.Module',
             'Demo110315.view.service.Service',
             'Demo110315.view.service.ServiceModel',
             "Demo110315.view.esmodule.ESModule",
             'Demo110315.model.ESModule',
             'Demo110315.model.ESModuleitem',
             'Demo110315.view.endpath.EndPath',
             'Demo110315.model.Endpathitem',
             'Demo110315.view.globalpset.GlobalPset',
             'Demo110315.view.edsource.EDSourceModel',
             'Demo110315.view.edsource.EDSource',
             'Demo110315.view.essource.ESSourceModel',
             'Demo110315.view.essource.ESSource'],
    
    controller: "editor-editor",
    viewModel: {
        type: "editor-editor"
    },
    
    layout: {
        type: 'vbox',
        align: 'stretch'
    },
    
    listeners:{
        beforerender: 'onBeforeRender'
    },

     items: [
            {
                xtype: 'toolbar',
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
                            text: '<b>HLT Configuration Editor</b>'
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
//                            listeners: {
//                                click: function(view, e, eOpts){
//                                        var explorer = Ext.create('explorer');
//                                        explorer.show();
//                            }
//                        }
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
                            disabled: true
                        },
                        {
                            xtype: 'tbtext',
                            text: '<b>Configuration:</b>'   
                        },
                        {
                            xtype: 'tbtext',
                            bind:{
                                text: '{cnfname}'
                            }
                        }
//                        {
//                            xtype: 'textfield',
//                            reference: 'confName',
//                            fieldLabel: '<b>Configuration</b>',
//                            editable: false,
//                            bind:{
//                                value: '{cnfname}'
//                            }
//                        }
                    ] 
            },
//            {
//                xtype: 'panel',
//                border: true,    
//                //region: 'centre',
//                flex: 2,
//                layout: 'fit',    
//                items: [
            {
                xtype: 'tabpanel',
                flex: 2,
                layout: 'fit', 
                activeTab: 0,
                border: true,
                tabPosition: 'left',
                listeners:{
                    beforetabchange: 'onBeforeTabChange',//before
                    cusPathTabRender: 'onPathTabRender'
                },
                items: [
                        {
                            title: 'PATHS',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'pathtab'
                                }
                            ]
                        }
                        ,{
                            title: 'END PATHS',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'endpathtab'
                                }
                            ]
                        }
                        ,{
                            title: 'MODULES',
                            layout: 'fit',
                            items:[

                                {
                                    xtype: 'moduletab'
//                                    reference: 'moduleTab',
//                                    itemId: 'modtab'
                                    
                                }
                            ]
                        }
                        ,{
                            title: 'ED SOURCE',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'edsourcetab'
                                }
                            ]
                        }
                        ,{
                            title: 'SERVICES',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'servicetab'
                                }
                            ]
                        }
                        ,{
                            title: 'STREAMS & DATASETS',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'streamdataset'
                                }
                            ]
                        }
                        ,{
                            title: 'ES MODULES',
                            layout: 'fit',
                            items:[

                                {
                                    xtype: 'esmoduletab'
                                    
                                }
                            ]
                        }
                        ,{
                            title: 'ES SOURCES',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'essourcetab'
                                }
                            ]
                        }
                        ,{
                            title: 'GLOBAL PSET',
                            layout: 'fit',
                            items:[
                                {
                                    xtype: 'globalpsettab'
                                }
                            ]
                        }
//                        ,{
//                            title: 'SEQUENCES',
//                            layout: 'fit',
//                            items:[
//                                {
//                                    xtype: 'sequencetab'
//                                }
//                            ]
//                        }
//                        ,
//                        {
//                            title: 'SUBTABLES',
//                            html : 'Another one'
//                        }
                    ]

            }
//                ]
//            }
    ]
});
