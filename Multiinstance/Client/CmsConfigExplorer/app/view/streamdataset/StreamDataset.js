
Ext.define("CmsConfigExplorer.view.streamdataset.StreamDataset",{
    extend: "Ext.panel.Panel",

    requires:['CmsConfigExplorer.view.streamdataset.EventContentPanel',
             'CmsConfigExplorer.view.streamdataset.PathsTree',
             'CmsConfigExplorer.view.streamdataset.EventContent',
             'CmsConfigExplorer.view.streamdataset.PathsTreePanel',
             'CmsConfigExplorer.view.streamdataset.StreamDatasetController',
             'CmsConfigExplorer.view.streamdataset.StreamTree',
             'CmsConfigExplorer.view.streamdataset.StreamDatasetModel'],
    
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
//        {
//            xtype: 'toolbar',
//            region: 'north',
//            paddingLeft: 5,
//            items:[ 
//                    {
//                        xtype: 'textfield',
//                        fieldLabel: 'Search',
//                        labelWidth: 47,
//                        enableKeyEvents: true,
//                        disabled: true
//                    }
//                ]
//        },
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
//                    xtype: 'datasetpathspanel',                    
//                    reference: 'datasetpathsPanel',
                    xtype: 'datasetpaths',
                    reference: 'datasetPathsTree',
                    title: 'Dataset Paths',
                    loadMask: true,
                    height: '100%'
                }
                ,{
//                    xtype: 'evcopanel',
                    xtype: 'eventcontent',
                    loadMask: true,
                    bind: {
                        title: '<b>{current_evc} Statements</b>'
                    },
//                    title: 'EVENT CONTENT STATEMENTS',
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
