
Ext.define("Demo110315.view.streamdataset.StreamDataset",{
    extend: "Ext.panel.Panel",

    requires:['Demo110315.view.streamdataset.EventContentPanel',
             'Demo110315.view.streamdataset.PathsTree'],
    
    controller: "streamdataset-streamdataset",
    viewModel: {
        type: "streamdataset-streamdataset"
    },

    alias: 'widget.streamdataset',

    reference: 'streamDatasetTab',
    
    layout:{
        type: 'border'
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
            region: 'west',
            flex: 1,
            split: true,
            xtype: 'streamtree',
            height: '100%',
    //        collapsible: true,
            loadMask: true,
            listeners:{
                    rowclick: 'onStreamitemClick',
                    render: 'onRender',
//                custGridModParams: 'onGridModParamsForward',
//                loadModules: 'onLoadModules'
                scope: 'controller'
            }
        },
        {
            region: 'center',
            xtype: 'panel',
            reference: "streamCentralPanel",
//            title: 'Event Content Statements',            
            layout: 'card',
            items:[
                {
                    xtype: 'datasetpathspanel',
                    title: 'Dataset Paths',
                    loadMask: true
                }
                ,{
                    xtype: 'evcopanel',
                    loadMask: true,
                    title: 'EVENT CONTENT STATEMENTS',
                    height: '100%' 
                }
            ],
            split: true,
            height: '100%',
            width: '50%'
        
        }
//        ,{
//            region: 'east',
//            flex: 1,
//            split: true,
//            xtype: 'panel',
//            height: '100%',
//    //        collapsible: true,
//            loadMask: true,
//            title: 'Configuration Paths'
//        }
    ]
    
});
