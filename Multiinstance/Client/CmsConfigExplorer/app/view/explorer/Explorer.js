
Ext.define("CmsConfigExplorer.view.explorer.Explorer",{
    extend: "Ext.panel.Panel",
    
    alias: "widget.dbexplorer",
    
    reference: "dbexplorer",
    
    requires:['CmsConfigExplorer.view.explorer.Versions',
              'CmsConfigExplorer.view.explorer.Folders',
             'CmsConfigExplorer.view.explorer.FoldersController',
             'CmsConfigExplorer.view.explorer.VersionsController',
             'CmsConfigExplorer.model.Folderitem',
             'CmsConfigExplorer.model.Version',
             'CmsConfigExplorer.view.explorer.VersionsGrid',
             'CmsConfigExplorer.view.explorer.VersionsGridController'],
    
    controller: "explorer-explorer",
    viewModel: {
        type: "explorer-explorer"
    },
    bind:{
        title: " HLT Configurations eXplorer - {appversion}"
    },
    
    layout: {
        type: 'border'
    },
    
    listeners:{
        beforerender: 'onExplorerRender'
        //( this, eOpts )
    },
    loadMask: true,
    items: [
        {
            xtype: 'toolbar',
            region: 'north',
            paddingLeft: 5,
            items:[ 
                    {
                            xtype: "image",
                            src: "resources/cms-logo.png",
                            width: 30, //"10%",
                            height: 30 //"80%",
                        },
                    {
                        xtype: 'textfield',
                        fieldLabel: 'Search',
                        labelWidth: 47,
                        enableKeyEvents: true,
                        disabled: true
                    },
                    {
                            text: 'Home',
                            listeners: {
                                click: 'onHomeClick',
                                scope: 'controller'
                            }
                        }
                    ,{
                            xtype: 'tbtext',
                            text: '<b>Path:</b>'   
                        },
                        {
                            xtype: 'tbtext',
                            bind:{
                                text: '{selectedFolderitem.name}'
                            }
                        }
                ]
        },
        {
            region: 'center',
            flex: 2,
            split: true,
            xtype: 'folders',
            height: '100%',
            loadMask: true,
            useArrows: true,
            listeners:{
                custConfVers: 'onConfVersForward',
                custOpenLastVers: 'onForwaredOpenLastVers'
                //scope: 'controller'
            }
        }
        ,{
            flex: 3,
            region: 'east',
            xtype: 'versions',
            loadMask: true,
            split: true,
            height: '100%',
            listeners:{
                custOpenVer: 'onVerForward'
            }


        }
    ]
    
});
