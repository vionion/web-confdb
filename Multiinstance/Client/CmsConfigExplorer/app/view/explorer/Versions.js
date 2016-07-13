
Ext.define("CmsConfigExplorer.view.explorer.Versions",{
    extend: "Ext.panel.Panel",

    requires:['CmsConfigExplorer.model.Folderitem',
             'CmsConfigExplorer.model.Version',
             'CmsConfigExplorer.view.explorer.VersionsGrid'],
    
    alias: "widget.versions",
    
    reference: "versionsPanel",
    
    controller: "explorer-versions",
    
    layout:{
        type: 'vbox',
        align: 'stretch'
        
    },
    
    items:[
        {
            title: 'Versions',
            xtype: 'versionsGrid',
            scrollable: true,
            flex: 4,
            listeners: {
                rowdblclick:  'onVerDblClick',
                rowclick: 'onVerClick'
            }
        },
        {
            xtype: 'panel',
            title: 'Description',
            flex:2,
            layout: 'fit',
            items: [
                {
                    xtype: 'textarea',
                    width: '100%',
                    reference: 'descTextArea',
                    scrollable: true,
                    editable: false
                }
            ]

        }
    ]
});
