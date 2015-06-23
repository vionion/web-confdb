
Ext.define("Demo110315.view.explorer.VersionsGrid",{
    extend: "Ext.grid.Panel",

    controller: "explorer-versionsgrid",

    alias: "widget.versionsGrid",
    
    requires:['Demo110315.model.Folderitem',
             'Demo110315.model.Version'],
    
    bind:{
        // bind store to view model "modules" store
        store:'{versions}'
    },

    reference: "versionsGrid",
    
    columns: [
        { xtype: 'gridcolumn', header: 'Name', dataIndex: 'name', flex: 1 },
        { xtype: 'gridcolumn', header: 'Created', dataIndex: 'created' },
        { xtype: 'gridcolumn', header: 'Author', dataIndex: 'creator' },
        { xtype: 'gridcolumn', header: 'Version', dataIndex: 'ver' },
        { xtype: 'gridcolumn', header: 'Release', dataIndex: 'rel' }

    ]
    

});
