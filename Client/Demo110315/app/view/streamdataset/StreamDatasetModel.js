Ext.define('Demo110315.view.streamdataset.StreamDatasetModel', {
    extend: 'Ext.app.ViewModel',
    alias: 'viewmodel.streamdataset-streamdataset',
    
    requires:['Demo110315.model.Streamitem',
             'Demo110315.model.Evcoitem',
             'Demo110315.model.Datasetitem'],
    
    data: {
        name: 'Demo110315',
        idVer: -1,
        idCnf: -1,
        first: true
    },
    
    stores:
    {        
        streamitems:{
            
            type:'tree',
            model:'Demo110315.model.Streamitem',
            autoLoad: false,

            root: {
                expanded: false,
                text: "Streams and Datasets",
                gid: -1
//                root: true
            },
            
            listeners: {
                load: function(store, records, successful, operation, node, eOpts){
                    this.getRoot().expand();
                }       
            }
        },
        datasetpaths:{
            
                type:'tree',
                model:'Demo110315.model.Datasetitem',
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
                model:'Demo110315.model.Evcoitem',
                autoLoad:false
            
//                listeners: {
//
//                }
        }
    }
    

});
