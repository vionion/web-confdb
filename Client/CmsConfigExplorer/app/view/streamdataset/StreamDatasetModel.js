Ext.define('CmsConfigExplorer.view.streamdataset.StreamDatasetModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.streamdataset-streamdataset',
    
    requires:['CmsConfigExplorer.model.Streamitem',
             'CmsConfigExplorer.model.Evcoitem',
             'CmsConfigExplorer.model.Datasetitem'],
    
    data: {
        name: 'CmsConfigExplorer',
        idVer: -1,
        idCnf: -1,
        first: true,
        online: "False",
        current_dat: "",
        current_evc: ""
    },
    
    stores:
    {        
        streamitems:{
            
            type:'tree',
            model:'CmsConfigExplorer.model.Streamitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Streams and Datasets",
                gid: -1
//                root: true
            },
            
            listeners: {
                
                beforeload: 'onStreamitemsBeforeLoad',
                load: 'onStreamitemsLoad'
//                load: function(store, records, successful, operation, node, eOpts){
//                    this.getRoot().expand();
//                }       
            }
        },
        datasetpaths:{
            
                type:'tree',
                model:'CmsConfigExplorer.model.Datasetitem',
                autoLoad:false,
//                clearOnLoad : true,
//                clearRemovedOnLoad : true,
//                trackRemoved: false, 
                root: {
                    expanded: false,
                    text: "Streams and Datasets",
                    gid: -1
    //                root: true
                },
            
                listeners: {
                    load: 'onDatasetpathsLoad',
                    scope: 'controller'
                }
            },
        ecstats:{
                model:'CmsConfigExplorer.model.Evcoitem',
                autoLoad:false
            
//                listeners: {
//
//                }
        }
    }
    

});
