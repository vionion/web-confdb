
Ext.define("Demo110315.view.streamdataset.PathsTreePanel",{
    extend: "Ext.panel.Panel",

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
            region: 'center',
            loadMask: true
        }
    ]
});
