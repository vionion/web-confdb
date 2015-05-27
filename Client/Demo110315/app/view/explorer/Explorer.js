
Ext.define("Demo110315.view.explorer.Explorer",{
    extend: "Ext.panel.Panel",
    
    alias: "widget.dbexplorer",
    
    reference: "dbexplorer",
    
    requires:['Demo110315.view.explorer.Versions',
              'Demo110315.view.explorer.Folders',
             'Demo110315.view.explorer.FoldersController',
             'Demo110315.view.explorer.VersionsController',
             'Demo110315.model.Folderitem',
             'Demo110315.model.Version',
             'Demo110315.view.explorer.VersionsGrid',
             'Demo110315.view.explorer.VersionsGridController'],
    
    controller: "explorer-explorer",
    viewModel: {
        type: "explorer-explorer"
    },

    title: " HLT Configurations eXplorer",
    
    layout: {
        type: 'border'
    },
    
    listeners:{
        //( this, eOpts )
    },
    loadMask: true,
//    header: false,
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
//                            margin: "0 0 0 50"
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
                                text: '{selectedFolderitem.new_name}'
                            }
                        }
                ]
        },
        {
            region: 'center',
            flex: 1,
            split: true,
            xtype: 'folders',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                custConfVers: 'onConfVersForward',
                custOpenLastVers: 'onForwaredOpenLastVers'
                //scope: 'controller'
            }
        }
        ,{
            flex: 1,
            region: 'east',
//            layout: 'fit',
            xtype: 'versions',
            loadMask: true,
    //        xtype:'panel',
            split: true,
            height: '100%',
            listeners:{
                custOpenVer: 'onVerForward'
            }


        }
    ]
    
});
