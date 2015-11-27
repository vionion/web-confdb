
Ext.define("CmsConfigExplorer.view.streamdataset.PathsTreePanel",{
    extend: "Ext.panel.Panel",

    requires:['CmsConfigExplorer.view.streamdataset.PathsTree',
             'CmsConfigExplorer.view.streamdataset.PathsTreePanelController'],
    
    controller: "streamdataset-pathstreepanel",

    alias: 'widget.datasetpathspanel',
    
    reference: 'datasetpathsPanel',
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
                        xtype: 'textfield',
                        fieldLabel: 'Search',
                        labelWidth: 47,
                        enableKeyEvents: true,
                        disabled: true
                    }
            ]  
        },
        {
            xtype: 'datasetpaths',
            reference: "datasetPathsTree",
            region: 'center',
            loadMask: true,
            height: '100%'
        }
    ]
});
