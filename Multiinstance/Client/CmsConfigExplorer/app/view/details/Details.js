
Ext.define("CmsConfigExplorer.view.details.Details",{
    extend: "Ext.tab.Panel",
 
    alias: 'widget.detailsview',
    
    requires: [
        "CmsConfigExplorer.view.details.DetailsController",
        "CmsConfigExplorer.view.details.DetailsModel",
        'CmsConfigExplorer.view.path.Path',
        'CmsConfigExplorer.view.module.Module',
        'CmsConfigExplorer.view.service.Service',
        'CmsConfigExplorer.view.esmodule.*',
        'CmsConfigExplorer.view.endpath.EndPath',
        'CmsConfigExplorer.view.globalpset.*',
        'CmsConfigExplorer.view.edsource.EDSource',
        'CmsConfigExplorer.view.essource.*',
        'CmsConfigExplorer.view.streamdataset.StreamDataset',
        'CmsConfigExplorer.view.sequence.Sequence',
        'CmsConfigExplorer.view.sequence.*'
    ],
    
//    reference: 'detailsview',
    
    controller: "details-details",
    viewModel: {
        type: "details-details"
    },
    
    flex: 2,
//    layout: 'fit',
//    reference: 'tabscontainer',
    activeTab: 0,
    border: true,
    tabPosition: 'left',
//    tabRotation: 0,
    listeners:{
        beforetabchange: 'onBeforeTabChange',//before
        cusPathTabRender: 'onPathTabRender',
        beforerender: 'onBeforeRender'
//        loadPaths: 'onLoadPaths'
    },
       
    items: [
            {
                title: 'PATHS',
                xtype: 'pathtab',
                listeners:{
                    loadPaths: 'onLoadPaths'
                }
            }
            ,{
                title: 'END PATHS',
                xtype: 'endpathtab'
            }
            ,{
                title: 'SEQUENCES',
                xtype: 'sequencetab'
            }
            ,{
                title: 'MODULES',
                xtype: 'moduletab'
            }
            ,{
                title: 'ED SOURCE',
                xtype: 'edsourcetab'
            }
            ,{
                title: 'SERVICES',
                xtype: 'servicetab'
            }
            ,{
                title: 'STREAMS & DATASETS',
                xtype: 'streamdataset'
            }
            ,{
                title: 'ES MODULES',
                xtype: 'esmoduletab'
            }
            ,{
                title: 'ES SOURCES',
                xtype: 'essourcetab'
            }
            ,{
                title: 'GLOBAL PSET',
                xtype: 'globalpsettab'
            }
            
//                        ,
//                        {
//                            title: 'SUBTABLES',
//                            html : 'Another one'
//                        }
            ]
//        }
//        
//    ]
    
});
